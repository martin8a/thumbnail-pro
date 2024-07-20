import modelbit
import json
import streamlit as st

def get_thumbnail_pro_model(title, thumbnail):
    try:
        response = modelbit.get_inference(
          workspace="martinochoa",
          deployment="prompt_thumbnail_pro",
          data=[thumbnail, title]
        )
    except:
        st.write("...")
        return 'Error'

    parsedData = json.loads(response['data'])
    return parsedData

def get_recommendations_llava(title, thumbnail):
    response = modelbit.get_inference(
      workspace="martinochoa",
      deployment="prompt_llava",
      data=[thumbnail, title]
    )
    return response["data"]
