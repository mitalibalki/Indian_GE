# import libraries

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
from plotfunc import *

# set page configuration
st.set_page_config(
    page_title="Indian Elections Dashboard",
    page_icon=":elephant:",
    layout="wide",
    initial_sidebar_state="expanded")

# load and cache the dataframe
@st.cache_data 
def load_data(url):
    df = pd.read_csv(url)
    if url == 'Cleaned_GE1.csv':
    	df = df.loc[df['ENOC'] != 0]
    if url == 'Margin_GE.csv':
    	df = df.loc[df['Turnout'] != 0]
    return df

data = load_data('Cleaned_GE1.csv')

data2 = load_data('Margin_GE.csv')

# initialize variables in session state
if 'selected_report' not in st.session_state:
	st.session_state['selected_report'] = "Choose Report"

if 'selected_year' not in st.session_state:
	st.session_state['selected_year'] = "All Years"

if 'selected_state' not in st.session_state:
	st.session_state['selected_state'] = "All States"

if 'selected_const' not in st.session_state:
	st.session_state['selected_const'] = "All Constituencies"

if 'selected_comp' not in st.session_state:
	st.session_state['selected_comp'] = "No. of Candidates"

if 'sim_num' not in st.session_state:
	st.session_state['sim_num'] = 100

# defining a function to reset all variables
def reset_var(year = 1, state = 1, const = 1):
	if year == 1:
		st.session_state['selected_year'] = "All Years"
	if state == 1:
		st.session_state['selected_state'] = "All States"
	if const == 1:
		st.session_state['selected_const'] = "All Constituencies"


# sidebar
with st.sidebar:
    st.title(':diya_lamp: Customization Options')

    reports = ["Choose Report", "Comprehensive", "Yearly Comparison", "Specific Margin"]
    st.session_state['selected_report'] = st.selectbox('What report are you looking for?', reports, index=0)

    if st.session_state['selected_report'] == reports[0]:
    	st.markdown("No report format selected")

    if st.session_state['selected_report'] == reports[1]:
    	# if comprehensive, choose year
    	year_list = ["All Years", 1962, 1967, 1977, 1980, 1984, 1989, 1991, 1996, 1998, 1999, 2004, 2009, 2014, 2019]

    	# select year
    	st.session_state['selected_year'] = st.selectbox('Select a year', year_list, index=0)

    	if st.session_state['selected_year'] != "All Years":
    		df_selected_year = data.loc[data['Year'] == st.session_state['selected_year']]
    		state_list = ["All States"] + sorted(list(set(df_selected_year['State_Name'].tolist())))
    		st.session_state['selected_state'] = st.selectbox('Select a state', state_list, index=0)

    	else:
	    	reset_var(0,1,1)

	# for year wise comparison
    if st.session_state['selected_report'] == reports[2]:
    	yearly_comp = ["No. of Candidates", "ENOP", "ENOC", "Fraction of Votes"]
    	st.session_state['selected_comp'] = st.selectbox('Select a way to compare', yearly_comp, index=0)

    if st.session_state['selected_report'] == reports[3]:
    	st.session_state['sim_num'] = st.number_input("How many times to run the RVM?", value = 100)

# based on report selected in the sidebar, display the information
if st.session_state['selected_report'] == reports[0]:
	st.header(f"Analysis & Visualization of Indian General Elections between {min(valid_elections)} and {max(valid_elections)}")
	st.divider()
	st.markdown("**Data for the analysis was obtained from:**")
	st.markdown('Ananay Agarwal, Neelesh Agrawal, Saloni Bhogale, Sudheendra Hangal, Francesca Refsum Jensenius, Mohit Kumar, Chinmay Narayan, Basim U Nissa, Priyamvada Trivedi, and Gilles Verniers. 2021. “TCPD Indian Elections Data v2.0", *Trivedi Centre for Political Data, Ashoka University*.')
	st.markdown("https://lokdhaba.ashoka.edu.in/browse-data?et=GE")

	st.divider()
	st.markdown("**Methodology for analyses and their references:**")

	st.markdown("***Log of Density vs Log of Fraction of Votes:***")
	st.markdown("Prenga, Dode & Ifti, Margarita. (2012). Distribution of Votes and a Model of Political Opinion Formation for Majority Elections. International Journal of Modern Physics Conference Series. 16. 1-12. 10.1142/S2010194512007738.")
	st.markdown("https://www.worldscientific.com/doi/abs/10.1142/S2010194512007738")

	st.markdown("***Distribution of Specific Margin:***")
	st.markdown("Pal, R., Kumar, A., & Santhanam, M. S. (2024). Universal Statistics of Competition in Democratic Elections. arXiv preprint arXiv:2401.05065.")
	st.markdown("https://arxiv.org/abs/2401.05065")

	st.divider()

# if comprehensive is selected
if st.session_state['selected_report'] == reports[1]:

	# title of the page
	st.header(f"Comprehensive Analysis for {st.session_state['selected_year']}")
	if st.session_state['selected_state'] != "All States":
		st.subheader(f"For the state of {st.session_state['selected_state']}")

	st.divider()
	st.markdown("**Analysing the Number of Candidates Competing Per Constituency**")
	st.markdown('''This section will look at the absolute number of candidates competing and also look at the effective number of candidates as calculated based on vote share (including ENOP as proposed by Laakso and Taagepera, 1979).''')

	col = st.columns((2, 2, 2), gap='medium')

	# trying plot of number of candidates
	fig = n_candidates(data, year = st.session_state['selected_year'], state = st.session_state['selected_state'])
	fig = ENOC(data, year = st.session_state['selected_year'], state = st.session_state['selected_state'])
	fig = ENOP(data, year = st.session_state['selected_year'], state = st.session_state['selected_state'])

	with col[0]:
		# displays graph for number of candidates
		plt.figure(1)
		st.pyplot(fig)
		
	with col[1]:
		# displays ENOC
		plt.figure(2)
		st.pyplot(fig)
		
	with col[2]:
		plt.figure(5)
		st.pyplot(fig)
		
	col1 = st.columns((2, 2, 2), gap='medium')

	with col1[0]:
		# displays desc for number of candidates
		cand_list = n_candidates(data, year = st.session_state['selected_year'], state = st.session_state['selected_state'], stats = True)
		st.markdown("**Descriptive Statistics:**")
		st.markdown(f"Min: **{min(cand_list)}**")
		st.markdown(f"Max: **{max(cand_list)}**")
		st.markdown(f"Average: **{np.mean(cand_list):.2f}**")
		st.markdown("Mode: **N/A**")

		st.markdown("**Description:**")
		st.markdown(f"Distribution of number of candidates per constituency for {st.session_state['selected_year']}. The data has not been changed, only filtered and graphed.")

	with col1[1]:
		# displays desc for ENOC
		enoc_list = ENOC(data, year = st.session_state['selected_year'], state = st.session_state['selected_state'], stats = True)

		st.markdown("**Descriptive Statistics:**")
		st.markdown(f"Min: **{min(enoc_list)}**")
		st.markdown(f"Max: **{max(enoc_list)}**")
		st.markdown(f"Average: **{np.mean(enoc_list):.2f}**")
		st.markdown(f"Mode: **{statistics.mode(enoc_list)}**")

		st.markdown("**Description:**")
		st.markdown(f"Distribution of ENOC (Effective number of candidates) per constituency for {st.session_state['selected_year']}. This data was obtained by counting the number of candidates whose vote share was greater than the average vote share per candidate (total votes / no. of candidates).")

	with col1[2]:
		# displays desc for ENOP
		enop_list = ENOP(data, year = st.session_state['selected_year'], state = st.session_state['selected_state'], stats = True)

		st.markdown("**Descriptive Statistics:**")
		st.markdown(f"Min: **{min(enop_list)}**")
		st.markdown(f"Max: **{max(enop_list)}**")
		st.markdown(f"Average: **{np.mean(enop_list):.2f}**")
		st.markdown("Mode: **N/A**")

		st.markdown("**Description:**")
		st.markdown(f"Distribution of ENOP (Effective number of parties) per constituency for {st.session_state['selected_year']}. Check *Laakso and Taagepera (1979)* for the process. It takes into account the voteshare won by every candidate that contests the elections.")

	st.divider()

	# display the visualization for difference in vote margins only if state is all
	if st.session_state['selected_state'] == "All States":
		st.markdown("**Visualizing the Vote Share Margin Per Constituency**")
		st.markdown("This section visualizes the distribution of the difference in vote shares obtained by the Winning candidate (V1) and runner-up (V2) as well as the difference between V2 and second runner up (V3).")

		fig = margin_of_victory(data, year = st.session_state['selected_year'])

		col3 = st.columns((2, 2, 2), gap='medium')

		with col3[0]:
			plt.figure(3)
			st.pyplot(fig)

		st.divider()

		if st.session_state['selected_year'] != "All Years":

			st.markdown(f"**Analysing the Distribution of Fraction of Votes for the Year {st.session_state['selected_year']}**")
			st.markdown("The below graph is a Log-Log graph and has been constructed in accordance with the method suggested by Prenga, Dode & Ifti, Margarita. (2012).")

			# make and display graph
			col4 = st.columns((2, 2, 2), gap='medium')

			with col4[0]:
				fig = density_log_plot(data, st.session_state['selected_year'])
				plt.figure(4)
				st.pyplot(fig)

			st.markdown("**Description:**")
			st.markdown("The light green line running vertically represents the 20% mark. The paper by Prenga, Dode & Ifti, Margarita. (2012) hypothesized that 20% of the points would follow a ***Powerlaw*** and the rest 80% would exhibit a ***Gaussian Distribution***.")
			st.divider()

# if yearly comparisons is selected
# function that takes in selected yearly comp and sets the graph function
def func_yearly(graph_name, year):
	if graph_name == "No. of Candidates":
		return yearly_n_candidates(data, year)
	elif graph_name == "ENOP":
		return yearly_ENOP(data, year)
	elif graph_name == "ENOC":
		return yearly_ENOC(data, year)
	elif graph_name == "Fraction of Votes":
		return yearly_density_log_plot(data, year)

# for yearly comparisons
if st.session_state['selected_report'] == reports[2]:

	st.header(f"Year Wise Distribution of {st.session_state['selected_comp']} (1962-2019)")

	# set page config
	row1 = st.columns(4, gap='medium')
	row2 = st.columns(4, gap='medium')
	row3 = st.columns(4, gap='medium')
	row4 = st.columns(4, gap='medium')

	for i in range(4):
		with row1[i]:
			st.markdown(f"<div style='text-align: center'>{valid_elections[i]}</div>", unsafe_allow_html= True)
			fig = func_yearly(st.session_state['selected_comp'], valid_elections[i])
			plt.figure(valid_elections[i])
			st.pyplot(fig)

	for i in range(4):
		with row2[i]:
			st.markdown(f"<div style='text-align: center'>{valid_elections[i+4]}</div>", unsafe_allow_html= True)
			fig = func_yearly(st.session_state['selected_comp'], valid_elections[i+4])
			plt.figure(valid_elections[i+4])
			st.pyplot(fig)

	for i in range(4):
		with row3[i]:
			st.markdown(f"<div style='text-align: center'>{valid_elections[i+8]}</div>", unsafe_allow_html= True)
			fig = func_yearly(st.session_state['selected_comp'], valid_elections[i+8])
			plt.figure(valid_elections[i+8])
			st.pyplot(fig)

	for i in range(2):
		with row4[i]:
			st.markdown(f"<div style='text-align: center'>{valid_elections[i+12]}</div>", unsafe_allow_html= True)
			fig = func_yearly(st.session_state['selected_comp'], valid_elections[i+12])
			plt.figure(valid_elections[i+12])
			st.pyplot(fig)

# for specific margin
if st.session_state['selected_report'] == reports[3]:

	st.header("Visualizing the Specific Margin")

	st.divider()

	st.markdown("**Description:**")
	st.markdown("This section uses the Random Voter Model (RVM) proposed by Pal, R., Kumar, A., & Santhanam, M. S. (2024) to simulate margin (M) and specific margin (S) based on the turnout data from the elections.\n\nRefer to Pal, R., Kumar, A., & Santhanam, M. S. (2024) for the exact process.")

	st.divider()

	st.markdown("**Plotting Normalized Margin against the Simulated Normalized Margin:**")
	st.markdown(f"For this graph, the RVM was run {st.session_state['sim_num']} times. The Margin (M) refers to the vote difference between the first and second candidate in the constituency.")

	# do the generation of data
	turnout = data2['Turnout'].tolist()
	sim_margin, simulated_s_margin = generate_rvm(turnout, N=st.session_state['sim_num'])

	fig = plot_margin(data2, sim_margin)

	col5 = st.columns((1, 1), gap='medium')

	with col5[0]:
		plt.figure(10)
		st.pyplot(fig)

	st.divider()

	st.markdown("**Plotting Normalized Specific Margin against the Simulated Normalized Specific Margin:**")
	st.markdown(f"For this graph, the RVM was run {st.session_state['sim_num']} times. The  Specific Margin (S) refers to the vote difference between the first and second candidate divided by the turnout in the constituency.")

	fig = plot_s_margin(data2, simulated_s_margin)

	col6 = st.columns((1, 1), gap='medium')

	with col6[0]:
		plt.figure(11)
		st.pyplot(fig)

	st.divider()

	st.markdown("***Important Note:***")
	st.markdown("*Significant deviation of data points from the RVM generated ones suggests that there was some tampering with the elections data during that period.*")
	st.markdown("*The RVM uses a uniform distribution to generate data points, where three numbers from [0,1] are generated to represent the votes given to three candidates in the constituency. They are weighted and multiplied with the turnout to get the margin.*")
	st.markdown("*The Specific margin is calculated as follows:*")
	st.latex(r'''S_i = \frac{M_i}{T_i}''')
	st.markdown("*Where M refers to the margin and T to the turnout. i refers to the constituency in this case.*")