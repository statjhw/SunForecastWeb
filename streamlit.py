 st.write('#괄호')
 view=[100,150,30]
 view
 st.write('## barcart')
 st.bar_chart(view)
 sview= pd.Series(view)
 st.write('## gogo')
 data=pd.DataFrame({'index':['A','B','C'],
                    'values':[10,20,30]})
 st.write('## chart2!!')
 st.bar_chart(data,x='index',y='values',use_container_width=True)
 # m=folium.Map(location=[37.42637222,126.9898],zoom_start=16)
 # folium.Marker([37.42637222,126.9898],
 #               popup='junyeon',
 #               tooltip='junyeon').add_to(m)
 # st_data=st_folium(m,width=725)
