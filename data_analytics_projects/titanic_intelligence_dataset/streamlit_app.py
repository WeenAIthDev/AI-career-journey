import streamlit as st
import joblib
import pandas as pd
model = joblib.load('random_forest_model.pkl')
features = joblib.load('features.pkl')
st.title("Titanic Intelligence")
Age = st.number_input(label = "Enter age", min_value=0)
Fare = st.number_input(label = "Enter fare", min_value=0.5)
Sex = st.selectbox(label='Gender',options=['F','M'])
Embarked = st.selectbox(label='Embarked', options=['C','Q','S'])
Pclass = st.selectbox(label='pclass',options=[1,2,3])
SibSp = st.number_input(label='Siblings/Spouse', min_value=0, max_value=100)
#parch = st.number_input(label='Parents/Children' min_value=0, max_value=100)
Parch = st.number_input(label='Parents/Children', min_value=0, max_value=100)


def alone(familySize):
    if familySize == 0:
      isAlone = 1
    else:
      isAlone = 0
    return isAlone    
       
if st.button('Predict'):
    feature_dict = dict.fromkeys(features, 0)
    familySize = SibSp + Parch
    feature_dict["Pclass"]= Pclass
    feature_dict["Age"]=Age
    feature_dict["SibSp"]=SibSp
    feature_dict["Parch"]=Parch
    feature_dict["Fare"]=Fare
    feature_dict["isAlone"]=alone(familySize)
    if Sex == 'F':
       feature_dict['Sex_female'] = 1
       if Pclass == 1:
          feature_dict['Passenger_Type_female1'] = 1
       elif Pclass == 2:
          feature_dict['Passenger_Type_female2'] = 1
       else:
          feature_dict['Passenger_Type_female3'] = 1
             
             
    else:
       feature_dict['Sex_male'] = 1
       if Pclass == 1:
          feature_dict['Passenger_Type_male1'] = 1
       elif Pclass == 2:
          feature_dict['Passenger_Type_male2'] = 1
       else:
          feature_dict['Passenger_Type_male3'] = 1

    if Embarked == 'C':
       feature_dict['Embarked_C'] = 1
    elif Embarked == 'Q':
       feature_dict['Embarked_Q'] = 1
    else:
       feature_dict['Embarked_S'] = 1      

    if Age >=0 and Age<13:
      feature_dict['ageCategory_Child'] = 1
    elif Age >= 13 and Age < 20:
      feature_dict['ageCategory_Teen'] = 1    
    elif Age >= 20 and Age < 60:
      feature_dict['ageCategory_Adult'] = 1
    else:
      feature_dict['ageCategory_Senior'] = 1
    
    familySize = SibSp + Parch
    if familySize == 0:
      feature_dict['familySize_Alone'] = 1
    elif familySize >= 1 and familySize <= 4:
      feature_dict['familySize_Small Family'] = 1
    else:
      feature_dict['familySize_Large Family'] = 1
    

    
    df_features = pd.DataFrame.from_dict([feature_dict])
    #df = pd.DataFrame(feature_dict)  
    y_pred = model.predict(df_features)
    if y_pred[0] == 0:
       st.write("Prediction: ","Not Survived")
    else:
       st.write("Prediction: ","Survived")
    prob = model.predict_proba(df_features)
    st.write("Survival Probablity: ", str(int(round(prob[0][1],2)*100)), "%")      
    #print(y_pred)
    #print(model.predict_proba(df_features))

      


            



   
        




#st.success("Model Loaded Successfully")