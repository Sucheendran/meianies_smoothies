# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Example Streamlit App :cup_with_straw:")
st.write(    
   "Choose the fruits you want in your Custom Smoothie !") 


name_on_order=st.text_input ('Name on Smoothie:')
st.write('The Name on your smoothie will be:',name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


INGREDIENTS_LIST=st.multiselect(
    'Choose upto 5 Ingrdients:',my_dataframe, max_selections=5
    )


if INGREDIENTS_LIST:
       
    ingredients_string=''
    
    for fruit_chosen in INGREDIENTS_LIST:
        ingredients_string += fruit_chosen + ' '
    #st.write (ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order+ """')"""


#my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
#            values ('""" + ingredients_string + """')"""


#st.write(my_insert_stmt)

time_to_insert=st.button('Submit Order')



if time_to_insert:
#if ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


