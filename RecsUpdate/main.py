from helpers.helper_functions import *
from helpers.extract_from_TTB import *
import sys
from flask import Flask, request, send_file
from io import StringIO, BytesIO
import requests

def generate_recs(input_file):
  df_origin = create_dataset(input_file)
  print('Number of candidate entries:',df_origin.shape[0])
  (df_clean,program_languages_feature_names,tech_areas_feature_names,interest_tech_areas_feature_names,\
              goals_feature_names,interest_subject_domains_feature_names,teammates_programming_experience_feature_names) = dataset_preprocessing(df_origin)

  # filter out the important features
  df_selected_columns = pd.concat([df_clean.ix[:,0:2], df_clean.ix[:,5:6], df_clean.ix[:,10:11]\
                                             , df_clean.ix[:,12:18]],axis=1)
  df_selected_column_names = pd.concat([df_clean.ix[:,0:3], df_clean.ix[:,4:12]],axis=1)
  
  student_id_features_dict,student_id_features_names_dict = \
        create_student_feature_vectors(df_selected_columns,df_selected_column_names)

  # generate solutions
  start = time.time()
  solution_dict = {}
  for sid, feature_vector in student_id_features_dict.items():
      sorted_scores_list = compute_scores_per_student(sid, feature_vector,student_id_features_dict)
      solution_dict[sid] = sorted_scores_list
      
  end = time.time()
  print('Time it took to get the solution:',end - start)

  # organize recs into lists
  students = []
  students_feat = []
  recommendations = []
  recommendations_feat1 = []; recommendations_feat2 = []; recommendations_feat3 = []; recommendations_feat4 = []
  recommendations_feat5 = []; recommendations_feat6 = []; recommendations_feat7 = []; 
  recommendations_feat8 = []

  for key, val in solution_dict.items():
      vals = [x[0] for x in val[:8]]
      students.append(key)
      students_feat.append(student_id_features_names_dict[key])
      recommendations.append(vals)
      recommendations_feat1.append(student_id_features_names_dict[vals[0]])
      recommendations_feat2.append(student_id_features_names_dict[vals[1]])
      recommendations_feat3.append(student_id_features_names_dict[vals[2]])
      recommendations_feat4.append(student_id_features_names_dict[vals[3]])
      recommendations_feat5.append(student_id_features_names_dict[vals[4]])
      recommendations_feat6.append(student_id_features_names_dict[vals[5]])
      recommendations_feat7.append(student_id_features_names_dict[vals[6]])
      recommendations_feat8.append(student_id_features_names_dict[vals[7]])

  rows = zip(students,students_feat,recommendations,recommendations_feat1,recommendations_feat2,recommendations_feat3,\
          recommendations_feat4,recommendations_feat5,recommendations_feat6,recommendations_feat7,recommendations_feat8)


  # write solution to a StringIO object
  output_file = StringIO()
  writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(['student id','student feat','recommended teammates','member feat 1','member feat 2'\
                  ,'member feat 3','member feat 4','member feat 5','member feat 6','member feat 7','member feat 8'])
  for row in rows:
      writer.writerow(row)

  # reset pointers to beginning of file
  input_file.seek(0)
  output_file.seek(0)

  return output_file

app = Flask(__name__)

@app.route("/")
def index():
  return "Hello world!"

@app.route("/update", methods=["GET"])
def main():
  populate_TTB_url = 'https://us-central1-team-synergy-bu.cloudfunctions.net/populateTTBdata'
  populate_recs_url = 'https://us-central1-team-synergy-bu.cloudfunctions.net/populateRecs'

  input_file = get_csv_data()
  output_file = generate_recs(input_file)

  # sending post request and saving response as response object 
  print("input file: ", input_file)
  data = {'data': input_file}
  r = requests.post(url = populate_TTB_url, files={'input.csv': input_file}) 
    
  # extracting response text  
  TTB_data_response = r.text 
  print("The TTB data response is: %s"%TTB_data_response)

  # sending post request and saving response as response object
  data = {'data': output_file}
  r = requests.post(url = populate_recs_url, files={'output.csv': output_file}) 
    
  # extracting response text  
  recs_response = r.text 
  print("The recs response is: %s"%recs_response)

  if recs_response == "Success!\n" and TTB_data_response == "Success!\n":
    return "Success!\n"
  else:
    return f"Response for TTB is {TTB_data_response} and Response for Recs is {recs_response}"

if __name__ == '__main__':
  # This is used when running locally only. When deploying to Google App
  # Engine, a webserver process such as Gunicorn will serve the app. This
  # can be configured by adding an `entrypoint` to app.yaml.
  app.run(host='127.0.0.1', port=8080, debug=True)