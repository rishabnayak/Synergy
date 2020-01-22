from configparser import ConfigParser
from pg import DB
from io import StringIO
import hashlib
import csv

features = ['id', 'firstname', 'lastname', 'email', 'phone', 'full_duration', 'age', \
            'pronouns', 'school', 'school_type', 'major', 'graduation', 'traveling_from', \
            'proficiencies', 'first_hackathon', 'meaning', 'resume', 'linkedin', 'github', \
            'website', 'source', 'roles', 'experience', 'hackathon_count', 'foreign_country', \
            'most_experienced', 'interests', 'motivations', 'focus', 'background_preference', \
            'additional_info']
 
def config(filename='database.ini', section='postgresql'):
  # create a parser
  parser = ConfigParser()
  # read config file
  parser.read(filename)

  # get section, default to postgresql
  db = {}
  if parser.has_section(section):
    params = parser.items(section)
    for param in params:
      db[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in the {1} file'.format(section, filename))

  return db


def get_csv_data():
  """ Connect to the PostgreSQL database server """
  conn = None
  try:
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = DB(**params)
      
    # execute a statement
    print('PostgreSQL ALL accepted users who signed up for team matching')
    q = conn.query("SELECT * FROM users JOIN event_applications ON users.id = event_applications.user_id WHERE custom_fields ->> 'team_forming' = 'Yes, sign me up!' AND status = 'accepted';")

    data = q.dictresult()
    
    f = StringIO()
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(features)

    print(f'Adding {len(data)} entries to csv file')

    for row in data:
      str_id = str(row['user_id'])
      # get the MD5 hash of id
      result = hashlib.md5(str_id.encode())
      hashed_id = result.hexdigest()

      full_duration = (row['custom_fields'].get('arrival_time', '') == "I'm staying for the entire event")
      user_features = [hashed_id, row['first_name'], row['last_name'], row['email'], row['phone'], full_duration, \
                     row['age'], row['pronoun'], row['university'], row['education_lvl'], row['major'], \
                     row['grad_year'], row['custom_fields'].get("travel", None), row['custom_fields'].get("programming_skills", None), \
                     row['custom_fields'].get("been_to_ttb", None), None, None, row['custom_fields'].get("linkedin_url", None), \
                     row['custom_fields'].get("github_url", None), row['custom_fields'].get("other_url", None), row['custom_fields'].get("how_did_you_hear", None), \
                     None, row['custom_fields'].get("programming_experience", None), row['custom_fields'].get("how_many_hackathons", None), None, \
                     row['custom_fields'].get("other_skills", None), row['custom_fields'].get("particular_topic", None), row['custom_fields'].get("goals", None), \
                     row['custom_fields'].get("experience_area", None), row['custom_fields'].get("teammate_preference", None), None]
      writer.writerow(user_features)
    # move the pointer back to beginning of file
    f.seek(0)
    return f    
  except (Exception) as error:
    print("Error:", error)
  finally:
    if conn is not None:
        conn.close()
        print('Database connection closed.')

if __name__ == '__main__':
  get_csv_data()