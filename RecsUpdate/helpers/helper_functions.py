import numpy as np
import pandas as pd
import csv
import re
import warnings
import seaborn as sns
import operator
import time
import math

from sklearn.metrics import jaccard_similarity_score

from scipy.spatial import distance

sns.set(style="ticks", color_codes=True)

warnings.filterwarnings('ignore')

from sklearn.feature_extraction.text import CountVectorizer

def create_dataset(filename):
    '''
    Input: Csv file with the participants' raw information
    Output: Panda dataframe with the participants' information
    '''
    df = pd.read_csv(filename)
    return df

def Vectorizer():
    Vectorizer= CountVectorizer(
                    analyzer = "word",  
                    tokenizer = None,  
                    preprocessor = None, 
                    stop_words = None,  
                    max_features = 5000,
                    token_pattern = r"\b\w+\b")
    
    return Vectorizer

def dataset_preprocessing(df_origin):
    '''
    Input: Panda dataframe with participants' raw information
    Output: Panda dataframe with processed participants' information
    '''  

    # Renaming columns to more representative column names
    df_new_column_names = df_origin.rename(columns=                        # General Interests
                       {'full_duration': 'full_duration',\
                        'experience': 'experience_programming',\
                        'age': 'age',\
                        'proficiencies': 'experience_programming_languages',\
                        'first_hackathon': 'first_hackathon',\
                        'most_experienced': 'experience_tech_areas',\
                        'focus': 'interest_tech_areas',\
                        'motivations': 'goals',\
                        'background_preference': 'teammates_programming_experience',\
                        'hackathon_count': 'num_of_hackathon_participations',\
                        'interests': 'interest_subject_domains',\
                        'id': 'id'})
    
    # Keeping features relavent to team formation 
    df_selected_features = df_new_column_names[['id','full_duration','experience_programming','age',                                                 'experience_programming_languages','first_hackathon',                                                 'experience_tech_areas','interest_tech_areas','goals',                                                 'teammates_programming_experience','num_of_hackathon_participations','interest_subject_domains']]
    
    # Converting categorical features to numerical features
    df_selected_features['experience_programming'] = df_selected_features['experience_programming'].map                        ({'No programming experience!': 1,'Less than 6 months': 1,'More than 6 months': 2,                           'More than 1 year': 2, 'More than 2 years': 3})
    
    def convert_num_hackathon(x):
        if x == "5 or more":
            return 5
        else:
            return int(x)

    df_selected_features['num_of_hackathon_participations'] = df_selected_features['num_of_hackathon_participations'].map (convert_num_hackathon)                    #({'0 - TechTogether Boston will be my first one!': 1,'1 hackathon': 1,'2-3 hackathons': 2,                           '4-5 hackathons': 3, 'More than 6 hackathons': 3})
    
    # Pre-processing for one hot encoding - replacing empty lists and NaN values with 'None'
    df_selected_features.experience_programming_languages.replace('[]', 'None', inplace=True)
    df_selected_features.experience_programming_languages.replace(np.NAN, 'None', inplace=True)
    
    df_selected_features.experience_tech_areas.replace('[]', 'None', inplace=True)
    df_selected_features.experience_tech_areas.replace(np.NAN, 'None', inplace=True)
    
    df_selected_features.goals.replace('[]', 'None', inplace=True)
    df_selected_features.goals.replace(np.NAN, 'None', inplace=True)
    
    df_selected_features.interest_tech_areas.replace('[]', 'None', inplace=True)
    df_selected_features.interest_tech_areas.replace(np.NAN, 'None', inplace=True)
    
    df_selected_features.interest_subject_domains.replace('[]', 'None', inplace=True)
    df_selected_features.interest_subject_domains.replace(np.NAN, 'None', inplace=True)
    
    # Replace NaN values with "I don't have a preference"
    df_selected_features.teammates_programming_experience.replace(np.nan,"I don't have any preference!", inplace=True)

    
    # Creating one hot encoding for categorical features
    
    # one-hot-encoding for programming languages: ['css','go','html','java','javascript','python','ruby','swift']
    vectorizer_program_languages = Vectorizer()  
    corpus_program_languages = []
    df_selected_features['experience_programming_languages'].apply(lambda x: corpus_program_languages.append(x))
    corpus_program_languages = [text.replace(" ", "") for text in corpus_program_languages]
    corpus_program_languages = [text.replace("/", "") for text in corpus_program_languages]
    corpus_program_languages = [text.replace("+", "p") for text in corpus_program_languages]
    # corpus_program_languages = [text.replace("c", "clang") for text in corpus_program_languages]
    X_program_languages = vectorizer_program_languages.fit_transform(corpus_program_languages)
    
    program_languages_feature_names = vectorizer_program_languages.get_feature_names()

#     print
#     print 'Programming languages feature names:',vectorizer_program_languages.get_feature_names()

    df_selected_features['experience_programming_languages_vectorized'] = list(X_program_languages.toarray())

    # one-hot-encoding for experience_tech_areas
    vectorizer_tech_areas = Vectorizer()  
    corpus_tech_areas = []
    df_selected_features['experience_tech_areas'].apply(lambda x: corpus_tech_areas.append(x))
    corpus_tech_areas = [text.replace(" ", "") for text in corpus_tech_areas]
    corpus_tech_areas = [text.replace("/", "") for text in corpus_tech_areas]
    
    X_tech_areas = vectorizer_tech_areas.fit_transform(corpus_tech_areas)
    
    tech_areas_feature_names = vectorizer_tech_areas.get_feature_names()
#     print
#     print 'Tech areas feature names:',vectorizer_tech_areas.get_feature_names()

    df_selected_features['experience_tech_areas_vectorized'] = list(X_tech_areas.toarray())
    df_selected_features
    
    # one-hot-encoding for interest in tech areas
    vectorizer_interest_tech_areas = Vectorizer()  
    corpus_interest_tech_areas = []
    df_selected_features['interest_tech_areas'].apply(lambda x: corpus_interest_tech_areas.append(x))
    corpus_interest_tech_areas = [text.replace(" ", "") for text in corpus_interest_tech_areas]
    corpus_interest_tech_areas = [text.replace("/", "") for text in corpus_interest_tech_areas]
    corpus_interest_tech_areas = [text.replace("'", "") for text in corpus_interest_tech_areas]
    corpus_interest_tech_areas = [text.replace("!", "") for text in corpus_interest_tech_areas]
    corpus_interest_tech_areas = [text.replace("(", "") for text in corpus_interest_tech_areas]
    corpus_interest_tech_areas = [text.replace(")", "") for text in corpus_interest_tech_areas]
    X_interest_tech_areas = vectorizer_interest_tech_areas.fit_transform(corpus_interest_tech_areas)
    interest_tech_areas_feature_names = vectorizer_interest_tech_areas.get_feature_names()
    
#     print
#     print 'Interest in Tech areas feature names:',vectorizer_interest_tech_areas.get_feature_names()

    df_selected_features['interest_tech_areas_vectorized'] = list(X_interest_tech_areas.toarray())
    
    # one-hot-encoding for goals
    vectorizer_goals = Vectorizer()  
    corpus_goals = []
    df_selected_features['goals'].apply(lambda x: corpus_goals.append(x))
    corpus_goals = [text.replace(" ", "") for text in corpus_goals]
    corpus_goals = [text.replace("/", "") for text in corpus_goals]
    corpus_goals = [text.replace("'", "") for text in corpus_goals]
    corpus_goals = [text.replace("!", "") for text in corpus_goals]
    corpus_goals = [text.replace("&", "") for text in corpus_goals]
    corpus_goals = [text.replace(",", "") for text in corpus_goals]
    
    X_goals = vectorizer_goals.fit_transform(corpus_goals)
    goals_feature_names = vectorizer_goals.get_feature_names()
    
#     print
#     print 'Goals feature names:',vectorizer_goals.get_feature_names()

    df_selected_features['goals_vectorized'] = list(X_goals.toarray())
    
    # one-hot-encoding for subject domains
    vectorizer_interest_subject_domains = Vectorizer()  
    corpus_interest_subject_domains = []
    df_selected_features['interest_subject_domains'].apply(lambda x: corpus_interest_subject_domains.append(x))
    corpus_interest_subject_domains = [text.replace(" ", "") for text in corpus_interest_subject_domains]
    corpus_interest_subject_domains = [text.replace("/", "") for text in corpus_interest_subject_domains]
    corpus_interest_subject_domains = [text.replace("'", "") for text in corpus_interest_subject_domains]
    corpus_interest_subject_domains = [text.replace("!", "") for text in corpus_interest_subject_domains]
    corpus_interest_subject_domains = [text.replace("&", "") for text in corpus_interest_subject_domains]
    corpus_interest_subject_domains = [text.replace(",", "") for text in corpus_interest_subject_domains]
    
    X_interest_subject_domains = vectorizer_interest_subject_domains.fit_transform(corpus_interest_subject_domains)
    interest_subject_domains_feature_names = vectorizer_interest_subject_domains.get_feature_names()
    
#     print
#     print 'Subject domains feature names:',vectorizer_interest_subject_domains.get_feature_names()

    df_selected_features['interest_subject_domains_vectorized'] = list(X_interest_subject_domains.toarray())
    
    # one-hot-encoding for teammate experience
    vectorizer_teammates_programming_experience = Vectorizer()  
    corpus_teammates_programming_experience = []
    df_selected_features['teammates_programming_experience'].apply(lambda x: corpus_teammates_programming_experience.append(x))
    corpus_teammates_programming_experience = [text.replace(" ", "") for text in corpus_teammates_programming_experience]
    corpus_teammates_programming_experience = [text.replace("/", "") for text in corpus_teammates_programming_experience]
    corpus_teammates_programming_experience = [text.replace("'", "") for text in corpus_teammates_programming_experience]
    corpus_teammates_programming_experience = [text.replace("!", "") for text in corpus_teammates_programming_experience]
    corpus_teammates_programming_experience = [text.replace("&", "") for text in corpus_teammates_programming_experience]
    corpus_teammates_programming_experience = [text.replace(",", "") for text in corpus_teammates_programming_experience]
    
    X_teammates_programming_experience = vectorizer_teammates_programming_experience.fit_transform(corpus_teammates_programming_experience)
    teammates_programming_experience_feature_names = vectorizer_teammates_programming_experience.get_feature_names()

#     print
#     print 'Subject teammates programming exprience feature names:',vectorizer_teammates_programming_experience.get_feature_names()
    
    df_selected_features['teammates_programming_experience_vectorized'] = list(X_teammates_programming_experience.toarray())
    
    return df_selected_features,program_languages_feature_names,tech_areas_feature_names,interest_tech_areas_feature_names,            goals_feature_names,interest_subject_domains_feature_names,teammates_programming_experience_feature_names

def create_student_feature_vectors(df,df_names):
    student_id_features_dict = {}
    student_id_features_names_dict = {}
    for index, row in df.iterrows():
        student_id_features_dict[row['id']] = row.tolist()[1:]
     
    for index, row in df_names.iterrows():
        student_id_features_names_dict[row['id']] = row.tolist()[1:]
        
    return student_id_features_dict,student_id_features_names_dict

def compute_scores_per_student(student_id,student_feature_vector,student_id_features_dict):
    
    scores_list = []
    for sid,feature_vector in student_id_features_dict.items():
        if sid != student_id:
            # full_duration
            try:
                val1 = distance.euclidean(student_feature_vector[0],feature_vector[0]) 
                w1 = 1
            except:
                w1 = 0; val1 = 0
            # first hackathon
            try:
                val2 = distance.euclidean(student_feature_vector[1],feature_vector[1])
                w2 = 1 
            except:
                w2 = 0; val2 = 0
            # num of hackathon participations
            val3 = distance.euclidean(student_feature_vector[2],feature_vector[2])
            w3 = 1        
            # experience programming languages
            val4 = 1 - jaccard_similarity_score(student_feature_vector[3], feature_vector[3])
            w4 = 8
            # experience tech areas
            val5 = 1 - jaccard_similarity_score(student_feature_vector[4], feature_vector[4])
            w5 = 1
            # interested to learn tech areas
            val6 = 1 - jaccard_similarity_score(student_feature_vector[5], feature_vector[5])
            w6 = 5
            # goals of hackathon
            val7 = 1 - jaccard_similarity_score(student_feature_vector[6], feature_vector[6])
            w7 = 5
            # interest in subject domains
            val8 = 1 - jaccard_similarity_score(student_feature_vector[7], feature_vector[7])
            w8 = 10
            # teammates programming experience
            val9 = 1 - jaccard_similarity_score(student_feature_vector[8], feature_vector[8])
            w9 = 1
            
            score = (w1*val1 + w2*val2 + w3*val3 + w4*val4 + w5*val5 + w6*val6 + w7*val7 + w8*val8 + w9*val9)/float(w1+w2+w3+w4+w5+w6+w7+w8+w9)
            tup = (sid,score)
            scores_list.append(tup)
            
    scores_sorted_list = sorted(scores_list, key = lambda x: x[1])
    
    return scores_sorted_list