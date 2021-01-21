import streamlit as st
import pandas as  pd 
from faker import Faker  
import base64
import time
timestr = time.strftime("%Y%m%d-%G%M%S")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
def gen_loc_prof(n,lang,r_seed=200):
    locale_fake = Faker(lang)
    data =[locale_fake.simple_profile() for i in range(n)]
    df = pd.DataFrame(data)
    return df
def downlaod(d,format):

    if format == 'CSV':
        data_file = d.to_csv(index=False)
        f = 'csv'
    elif format == 'JSON':

        data_file =d.to_json()
        f = 'json'

    b64 = base64.b64encode(data_file.encode()).decode()
    st.markdown("### Download ###")
    new_file_name = f'fk_data{timestr}.{f}'
    href = f'<a href="data:file/{f};base64,{b64}" download="{new_file_name}">Click Here!</a>'
    st.markdown(href,unsafe_allow_html=True)

st.title('Fake Datagen')
st.header('Create Useful Dataset for you needs')
st.sidebar.header('Parameters')
menu = ['Home','Customize','Text Generation','About']
choice = st.sidebar.selectbox('Menu',menu)


if choice == 'Text Generation':
    st.subheader('Lorem Ipsum Geneator')
    langs = ['en_US','en','it_IT', 'en_US', 'ja_JP']
    lang = st.sidebar.selectbox('Locale',langs,0)
    cpy=st.sidebar.button("Copy")
   

    gen = st.button("Generate")
    cus = st.checkbox('Custom Words')
    if cus:
        tex = st.text_area("Enter a comma seperated words list").split(",")
        if len(tex)>0:
            text_fake = Faker(lang)
            sent = text_fake.sentence(ext_word_list=tex)
            
    else:
        text_fake = Faker(lang)
        sent=text_fake.sentence()
        st.write(sent)
       


elif choice == 'Home':
    st.subheader('Simple Profile Generator')
    num_to_gen = st.sidebar.number_input("Number",10,5000)
    langs = ['en_US','en','it_IT', 'en_US', 'ja_JP']
    lang = st.sidebar.multiselect('Locale',langs,default='en_US')
    d_format = st.sidebar.selectbox('Save As',['CSV','JSON'])
    
    df = gen_loc_prof(num_to_gen,lang)
    df.columns = [x.upper() for x in df.columns]
    st.dataframe(df)
    downlaod(df,d_format)


elif choice == 'Customize':
    st.subheader('Simple Custom Fields')
    num_to_gen = st.sidebar.number_input("Number",10,5000)
    langs = ['en_US','en','it_IT', 'en_US', 'ja_JP']
    lang = st.sidebar.multiselect('Locale',langs,default='en_US')
    d_format = st.sidebar.selectbox('Save As',['CSV','JSON'])
    
    profile_option_list = ['username','name','sex','address','mail','birthdate','job','company','ssn','residence']
    profile_fields = st.sidebar.multiselect("Fileds",profile_option_list,default='username')

    custom_fake = Faker(lang)

    data = [custom_fake.profile(fields=profile_fields) for i in range(num_to_gen)]
    df = pd.DataFrame(data)
    st.dataframe(df)
    with st.beta_expander("View JSON"):
        for i in range(num_to_gen):
            st.write(custom_fake.profile(profile_fields))
    with st.beta_expander('Download File'):
        downlaod(df,d_format)

elif choice == 'About':
    st.subheader('About')


