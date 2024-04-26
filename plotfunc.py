import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math

valid_elections = [1962, 1967, 1971, 1977, 1980, 1984, 1989, 1991, 1996, 1998, 1999, 2004, 2009, 2014, 2019]

# colour palette
c_dict = {
  'a': "#E5FCC2",
  'b': '#9DE0AD',
  'c': "#45ADA8",
  'd': "#547980",
}

def case_insensitive(word):
  if (type(word) == str) and 'all' in word.lower():
    if len(word.split())>1:
      word = word.split()[0]
    # return lower case
    return word.lower()
  else:
    return word

def n_candidates(data, year = "all", state = "all", constituency = "all", stats = False):
  year = case_insensitive(year)
  state = case_insensitive(state)
  constituency = case_insensitive(constituency)
  # initiating a list
  n_cand_count = []
  # when all the data is selected
  if year == 'all' and state == "all" and constituency == "all":
    title = "Count of Candidates for entire dataset"
    # start counting process
    for year_i in valid_elections:
      temp_year_data = data.loc[data['Year'] == year_i]
      for state_i in list(set(temp_year_data['State_Name'].tolist())):
        temp_state_data = temp_year_data.loc[temp_year_data['State_Name'] == state_i]
        for constno_i in list(set(temp_state_data['Constituency_No'].tolist())):
          count_i = len(temp_state_data.loc[temp_state_data['Constituency_No'] == constno_i])
          n_cand_count.append(count_i)

  elif year != 'all' and state == "all" and constituency == "all":
    title = f"Count of Candidates for {year}"
    temp_year_data = data.loc[data['Year'] == year]
    for state_i in list(set(temp_year_data['State_Name'].tolist())):
      temp_state_data = temp_year_data.loc[temp_year_data['State_Name'] == state_i]
      for constno_i in list(set(temp_state_data['Constituency_No'].tolist())):
        count_i = len(temp_state_data.loc[temp_state_data['Constituency_No'] == constno_i])
        n_cand_count.append(count_i)

  elif year != 'all' and state != "all" and constituency == "all":
    title = f"Count of Candidates for {year} in {state}"
    temp_state_data = data.loc[(data['Year'] == year) & (data['State_Name'] == state)]
    for constno_i in list(set(temp_state_data['Constituency_No'].tolist())):
      count_i = len(temp_state_data.loc[temp_state_data['Constituency_No'] == constno_i])
      n_cand_count.append(count_i)

  elif year != 'all' and state != "all" and constituency != "all":
    count_i = len(data.loc[(data['Year'] == year) & (data['State_Name'] == state) & (data['Constituency_Name'] == constituency)])
    return count_i

  if stats:
    # return the list if asked for stats
    return n_cand_count

  # plot the count
  bins = len(np.histogram_bin_edges(n_cand_count, bins='auto'))
  plt.figure(1)
  plt.hist(n_cand_count, bins = bins, color = c_dict['b'])
  # add titles
  plt.title(title)
  plt.xlabel("No. of candidates")
  plt.ylabel("Frequency")
  return plt

def ENOC(data, year = "all", state = "all", constituency = "all", stats = False):
  
  year = case_insensitive(year)
  state = case_insensitive(state)
  constituency = case_insensitive(constituency)

  # remove unwanted columns
  columns_wanted = ['State_Name','Year','Position','Constituency_Name','ENOC']
  temp_data = data[columns_wanted]
  temp_data = temp_data.dropna(subset=["ENOC"])
  temp_data = temp_data.loc[temp_data["Position"] == 1]

  if year == 'all' and state == "all" and constituency == "all":
    title = "ENOC Distribution for the entire dataset"
    # data to plot
    ENOC_data = temp_data['ENOC'].tolist()

  elif year != 'all' and state == "all" and constituency == "all":
    title = f"ENOC Distribution for {year}"
    temp_data = temp_data.loc[temp_data['Year'] == year]
    ENOC_data = temp_data['ENOC'].tolist()

  elif year != 'all' and state != "all" and constituency == "all":
    title = f"ENOC Distribution for {year} in {state}"
    temp_data = temp_data.loc[(temp_data['Year'] == year) & (temp_data['State_Name'] == state)]
    ENOC_data = temp_data['ENOC'].tolist()

  if stats:
    return ENOC_data

  # get the count for every unique ENOC value
  x = list(Counter(ENOC_data).keys())
  x.sort()
  y = [Counter(ENOC_data)[z] for z in x]
  plt.figure(2)
  plt.plot(x,y, color = c_dict['d'])
  plt.scatter(x,y, alpha=0.5, c = "red")
  if max(x) > 10:
    plt.xlim(0,28)
  else:
    plt.xlim(0,10)
  # add titles
  plt.title(title)
  plt.xlabel("ENOC")
  plt.ylabel("Frequency")
  #plt.axvline(x = 2, color = 'red')
  return plt

def margin_of_victory(data , year = "all", state = "all", constituency = "all"):

  year = case_insensitive(year)
  state = case_insensitive(state)
  constituency = case_insensitive(constituency)

  # remove unwanted columns
  columns_wanted = ['State_Name','Year','Position','Constituency_Name','Margin_Percentage']
  temp_data = data[columns_wanted]
  temp_data = temp_data.dropna(subset=['Margin_Percentage'])

  if year == 'all' and state == "all" and constituency == "all":
    title = "% Difference Distribution of candidates"
    # data to plot
    mov_2_1 = temp_data.loc[temp_data["Position"] == 1]['Margin_Percentage'].tolist()
    mov_3_2 = temp_data.loc[temp_data["Position"] == 2]['Margin_Percentage'].tolist()

  elif year != 'all' and state == "all" and constituency == "all":
    title = f"% Difference Distribution of candidates for {year}"
    temp_data = temp_data.loc[temp_data['Year'] == year]
    mov_2_1 = temp_data.loc[temp_data["Position"] == 1]['Margin_Percentage'].tolist()
    mov_3_2 = temp_data.loc[temp_data["Position"] == 2]['Margin_Percentage'].tolist()

  elif year != 'all' and state != "all" and constituency == "all":
    title = f"% Difference Distribution of candidates for {year} in {state}"
    temp_data = temp_data.loc[(temp_data['Year'] == year) & (temp_data['State_Name'] == state)]
    mov_2_1 = temp_data.loc[temp_data["Position"] == 1]['Margin_Percentage'].tolist()
    mov_3_2 = temp_data.loc[temp_data["Position"] == 2]['Margin_Percentage'].tolist()

  # plot the count
  bins_1 = len(np.histogram_bin_edges(mov_2_1, bins='auto'))
  bins_2 = len(np.histogram_bin_edges(mov_3_2, bins='auto'))

  plt.figure(3)
  plt.hist(mov_2_1, bins = bins_1, color=c_dict['b'], alpha = 0.5, label = "VS of 2 - VS of 1")
  plt.hist(mov_3_2, bins = bins_2, color=c_dict['c'], alpha = 0.5, label = "VS of 3 - VS of 2")

  # add titles
  plt.title(title)
  plt.legend(loc='upper right')
  plt.xlabel("% Difference of Votes")
  plt.ylabel("Frequency")
  return plt

def density_log_plot(data, year, max_value = 1, N = 100):
  # subset for data needed according to year
  data_year = data.loc[data['Year'] == year]

  # get data for which we need to determine bins
  vote_shares = list(data_year['Vote_Share_Percentage'])
  vote_shares = [vote*0.01 for vote in vote_shares]

  # getting the bin_values and h if N is specified
  if type(N) == int or type(N) == float:
    # setting bin size
    h = max_value/N
    # create a list for the limit/width of each bin
    bin_values = []
    # if number of bins needed in 30, then this we need the loop to run for 30+1 values
    for i in range(1,N+2):
      bin_values.append(i*h)

  elif type(N) == str:
    # for knuth optimization
    if N == 'kn':
      width, bin_values = knuth_bin_width(vote_shares, return_bins=True)
    elif N in ['scott', 'fd']:
      bin_values = np.histogram_bin_edges(vote_shares, bins= N)
    else:
      raise Exception("Invalid method of selecting bins")
    bin_values = sorted(bin_values)[1:]
    h = bin_values[1] - bin_values[0]

  # making a column called bin category
  bin_category = []

  for i in range(len(vote_shares)):
    vote_share = vote_shares[i]
    for j in range(len(bin_values)):
      if vote_share <= bin_values[j]:
        category_bin = bin_values[j]
        break
    bin_category.append(category_bin)

  # creating data for plotting log log plot
  frac_of_votes = []
  density = []
  unique_fractions = sorted(list(set(bin_category)))

  for i in range(len(unique_fractions)):
    frac_of_vote = unique_fractions[i] - (h/2)
    # get frequency per interval
    freq = bin_category.count(unique_fractions[i])
    rho = freq/len(bin_category)

    # update variables
    frac_of_votes.append(frac_of_vote)
    density.append(rho)

  # creating list of log values
  log_density = [math.log10(x) for x in density]
  log_frac_of_votes = [math.log10(x) for x in frac_of_votes]

  # creating the scatterplot
  plt.figure(4)
  plt.title(f"Density Log Plot for {year}")
  plt.scatter(log_frac_of_votes, log_density, s=80, edgecolors=c_dict['c'], alpha = 0.8,facecolors='none')
  plt.axvline(x = math.log10(0.2), c= c_dict['b'])
  # To show the plot
  plt.xlabel("log(frac of votes)")
  plt.ylabel("log(density)")

  return plt

def ENOP(data, year = "all", state = "all", constituency = "all", stats = False):

  year = case_insensitive(year)
  state = case_insensitive(state)
  constituency = case_insensitive(constituency)

  # remove unwanted columns
  columns_wanted = ['Year','Position','ENOP','State_Name']
  temp_data = data[columns_wanted]
  temp_data = temp_data.dropna(subset=["ENOP"])
  temp_data = temp_data.loc[temp_data["Position"] == 1]

  if year == 'all' and state == "all" and constituency == "all":
    title = "ENOP Distribution for the entire dataset"
    # data to plot
    ENOP_data = temp_data['ENOP'].tolist()

  elif year != 'all' and state == "all" and constituency == "all":
    title = f"ENOP Distribution for {year}"
    temp_data = temp_data.loc[temp_data['Year'] == year]
    ENOP_data = temp_data['ENOP'].tolist()

  elif year != 'all' and state != "all" and constituency == "all":
    title = f"ENOP Distribution for {year} in {state}"
    temp_data = temp_data.loc[(temp_data['Year'] == year) & (temp_data['State_Name'] == state)]
    ENOP_data = temp_data['ENOP'].tolist()

  if stats:
    return ENOP_data
    
  # plot the count
  bins = len(np.histogram_bin_edges(ENOP_data, bins='auto'))
  plt.figure(5)
  plt.hist(ENOP_data, bins = bins, color = c_dict['b'])
  
  # add titles
  plt.title(title)
  plt.xlabel("ENOP")
  plt.ylabel("Frequency")

  return plt

# yearly comparison ENOC
def yearly_ENOC(data, year, state = "all", constituency = "all"):
  
  year = case_insensitive(year)
  state = case_insensitive(state)
  constituency = case_insensitive(constituency)

  # remove unwanted columns
  columns_wanted = ['Year','Position','ENOC']
  temp_data = data[columns_wanted]
  temp_data = temp_data.dropna(subset=["ENOC"])
  temp_data = temp_data.loc[temp_data["Position"] == 1]

  if year != 'all' and state == "all" and constituency == "all":
    title = f"ENOC Distribution for {year}"
    temp_data = temp_data.loc[temp_data['Year'] == year]
    ENOC_data = temp_data['ENOC'].tolist()

  # get the count for every unique ENOC value
  x = list(Counter(ENOC_data).keys())
  x.sort()
  y = [Counter(ENOC_data)[z] for z in x]
  plt.figure(year)
  plt.plot(x,y, color = c_dict['d'])
  plt.scatter(x,y, alpha=0.5, c = "red")
  if max(x) > 10:
    plt.xlim(0,28)
  else:
    plt.xlim(0,10)
  # add titles
  plt.ylim(0,400)
  #plt.title(title)
  plt.xlabel("ENOC")
  plt.ylabel("Frequency")
  #plt.axvline(x = 2, color = 'red')
  return plt

# returns graphs for yearly comp
def yearly_n_candidates(data, year, state = "all", constituency = "all"):
  year = case_insensitive(year)
  # initiating a list
  n_cand_count = []
  # when all the data is selected
  if year != 'all' and state == "all" and constituency == "all":
    title = f"Count of Candidates for {year}"
    temp_year_data = data.loc[data['Year'] == year]
    for state_i in list(set(temp_year_data['State_Name'].tolist())):
      temp_state_data = temp_year_data.loc[temp_year_data['State_Name'] == state_i]
      for constno_i in list(set(temp_state_data['Constituency_No'].tolist())):
        count_i = len(temp_state_data.loc[temp_state_data['Constituency_No'] == constno_i])
        n_cand_count.append(count_i)

  # plot the count
  bins = len(np.histogram_bin_edges(n_cand_count, bins='auto'))
  plt.figure(year)
  plt.hist(n_cand_count, bins = bins, color = c_dict['b'])

  plt.xlim(0,80)
  plt.ylim(0,150)
  # add titles
  plt.xlabel("No. of candidates")
  plt.ylabel("Frequency")
  return plt

# yearly comp frac of votes
def yearly_density_log_plot(data, year, max_value = 1, N = 100):
  # subset for data needed according to year
  data_year = data.loc[data['Year'] == year]

  # get data for which we need to determine bins
  vote_shares = list(data_year['Vote_Share_Percentage'])
  vote_shares = [vote*0.01 for vote in vote_shares]

  # getting the bin_values and h if N is specified
  if type(N) == int or type(N) == float:
    # setting bin size
    h = max_value/N
    # create a list for the limit/width of each bin
    bin_values = []
    # if number of bins needed in 30, then this we need the loop to run for 30+1 values
    for i in range(1,N+2):
      bin_values.append(i*h)

  # making a column called bin category
  bin_category = []

  for i in range(len(vote_shares)):
    vote_share = vote_shares[i]
    for j in range(len(bin_values)):
      if vote_share <= bin_values[j]:
        category_bin = bin_values[j]
        break
    bin_category.append(category_bin)

  # creating data for plotting log log plot
  frac_of_votes = []
  density = []
  unique_fractions = sorted(list(set(bin_category)))

  for i in range(len(unique_fractions)):
    frac_of_vote = unique_fractions[i] - (h/2)
    # get frequency per interval
    freq = bin_category.count(unique_fractions[i])
    rho = freq/len(bin_category)

    # update variables
    frac_of_votes.append(frac_of_vote)
    density.append(rho)

  # creating list of log values
  log_density = [math.log10(x) for x in density]
  log_frac_of_votes = [math.log10(x) for x in frac_of_votes]

  # creating the scatterplot
  plt.figure(year)
  plt.scatter(log_frac_of_votes, log_density, s=80, edgecolors=c_dict['c'], alpha = 0.8,facecolors='none')
  plt.axvline(x = math.log10(0.2), c= c_dict['b'])

  plt.ylim(-4.5, 0)

  # To show the plot
  plt.xlabel("log(frac of votes)")
  plt.ylabel("log(density)")

  return plt

# yearly ENOP
def yearly_ENOP(data, year, state = "all", constituency = "all"):

  # remove unwanted columns
  columns_wanted = ['Year','Position','ENOP']
  temp_data = data[columns_wanted]
  temp_data = temp_data.dropna(subset=["ENOP"])
  temp_data = temp_data.loc[temp_data["Position"] == 1]

  if year != 'all' and state == "all" and constituency == "all":
    temp_data = temp_data.loc[temp_data['Year'] == year]
    ENOP_data = temp_data['ENOP'].tolist()

  # plot the count
  bins = len(np.histogram_bin_edges(ENOP_data, bins='auto'))
  plt.figure(year)
  plt.hist(ENOP_data, bins = bins, color = c_dict['b'])

  plt.xlim(0,10)
  plt.ylim(0,140)

  # add titles
  plt.xlabel("ENOP")
  plt.ylabel("Frequency")

  return plt

# yearly nagayama triangle
def yearly_nagayama(df, year):
  # get year data
  temp_data = df.loc[df["Year"] == year]

  v1 = temp_data["v1"].to_list()
  v2 = temp_data["v2"].to_list()
  v3 = temp_data["v3"].to_list()

  # creating the scatterplot
  plt.figure(year)

  #plt.title(f"Nagayama Triangle {year:.0f}")
  
  cand2 = plt.scatter(v1, v2, edgecolors='red', alpha = 0.5,facecolors='none')
  cand3 = plt.scatter(v1, v3, edgecolors='#45ADA8', alpha = 0.8,facecolors='none')

  #boundary lines
  plt.plot([0,50], [0,50],linestyle="--", color = "black")
  plt.plot([50,100], [50,0], linestyle="--", color = "black")
  plt.plot([33.33,100], [33.33,0], linestyle="--", color = "black")

  # To show the plot
  plt.xlabel("Vote share of 1st party")
  plt.ylabel("Vote share")
  plt.xlim(0,100)
  plt.ylim(0,60)
  plt.legend((cand2, cand3),("Candidate 2", "Candidate 3"))

  return plt

# yearly dist of vote shares for 3rd cand (for now)
def yearly_voteshare(data, year = "all", state = "all", constituency = "all", position = 3):
   # remove unwanted columns
  columns_wanted = ['State_Name','Year','Position','Constituency_Name','Vote_Share_Percentage']
  temp_data = data[columns_wanted]
  temp_data = temp_data.dropna(subset=['Vote_Share_Percentage'])
  temp_data = temp_data.loc[temp_data["Position"] == position]

  if year == 'all' and state == "all" and constituency == "all":
    title = "Voteshare Distribution of Winners"
    # data to plot
    Voteshare_data = temp_data['Vote_Share_Percentage'].tolist()

  elif year != 'all' and state == "all" and constituency == "all":
    title = f"Voteshare Distribution of Winners for {year}"
    temp_data = temp_data.loc[temp_data['Year'] == year]
    Voteshare_data = temp_data['Vote_Share_Percentage'].tolist()

  elif year != 'all' and state != "all" and constituency == "all":
    title = f"Voteshare Distribution of Winners for {year} in {state}"
    temp_data = temp_data.loc[(temp_data['Year'] == year) & (temp_data['State_Name'] == state)]
    Voteshare_data = temp_data['Vote_Share_Percentage'].tolist()

  # plot the count
  bins = len(np.histogram_bin_edges(Voteshare_data, bins='auto'))

  # creating the scatterplot
  plt.figure(year)

  plt.hist(Voteshare_data, bins = 20, color = c_dict['b'])


  # add titles
  #plt.title(title)
  plt.xlabel(f"Voteshare of candidate {position}")
  plt.ylabel("Frequency")

  if position == 1:
    plt.xlim(0,100)
    plt.ylim(0,120)

  if position == 2:
    plt.xlim(0,50)
    plt.ylim(0,70)

  if position == 3:
    plt.xlim(0,35)
    plt.ylim(0,200)

  return plt

# calculates the margin of votes using the uniform dist and turnout information
def calc_margin(turnout_n):
  random_array = np.random.uniform(0.0, 1.0, 3)
  random_array.sort()
  margin_s = (random_array[2] - random_array[1])/sum(random_array)
  margin = margin_s*turnout_n
  return margin, margin_s

def generate_rvm(turnout_list, N = 100):
  # generates N lists/ simulations for the list of turnouts provided
  # initiating list to store simulated margins
  simulated_margin = []
  simulated_s_margin = []

  for i in range(N):
    #print(f'Running Simulation {i+1}')
    for j in range(len(turnout_list)):
      m, s = calc_margin(turnout_list[j]) # calculates the margine and the specific margin
      simulated_margin.append(m)
      simulated_s_margin.append(s)

  #print(len(simulated_margin))
  return simulated_margin,simulated_s_margin

def plot_margin(df, sim_margin):
  # do the process for sim_margin first
  norm_sim_margin = sim_margin/np.mean(sim_margin)

  bin_values = np.histogram_bin_edges(norm_sim_margin, bins= 'scott')
  bin_values = sorted(bin_values)[1:]
  h = bin_values[1] - bin_values[0]

  # making a column called bin category
  bin_category = []

  for i in range(len(norm_sim_margin)):
    vote_share = norm_sim_margin[i]
    for j in range(len(bin_values)):
      if vote_share <= bin_values[j]:
        category_bin = bin_values[j]
        break
    bin_category.append(category_bin)

  # creating data for plotting log log plot
  frac_of_votes_sim = []
  density_sim = []
  unique_fractions = sorted(list(set(bin_category)))

  for i in range(len(unique_fractions)):
    frac_of_vote = unique_fractions[i] - (h/2)
    # get frequency per interval
    freq = bin_category.count(unique_fractions[i])
    rho = freq/len(bin_category)

    # update variables
    frac_of_votes_sim.append(frac_of_vote)
    density_sim.append(rho)

  # making plot for margin distribution
  margin = df['Margin'].tolist()

  norm_margin = margin/np.mean(margin)
  max_value = max(norm_margin)

  bin_values = np.histogram_bin_edges(norm_sim_margin, bins= 'scott')
  bin_values = sorted(bin_values)[1:]
  h = bin_values[1] - bin_values[0]

  #bin_values = []
  #N = 200
  #h = max_value/N
  #for i in range(1,N+2):
  #  bin_values.append(i*h)

  # making a column called bin category
  bin_category = []

  for i in range(len(norm_margin)):
    vote_share = norm_margin[i]
    for j in range(len(bin_values)):
      if vote_share <= bin_values[j]:
        category_bin = bin_values[j]
        break
    bin_category.append(category_bin)

  # creating data for plotting log log plot
  frac_of_votes = []
  density = []
  unique_fractions = sorted(list(set(bin_category)))

  for i in range(len(unique_fractions)):
    frac_of_vote = unique_fractions[i] - (h/2)
    # get frequency per interval
    freq = bin_category.count(unique_fractions[i])
    rho = freq/len(bin_category)

    # update variables
    frac_of_votes.append(frac_of_vote)
    density.append(rho)

  # make the plots
  plt.figure(10)
  plt.title('Distribution of Normalized Margin')
  plt.yscale("log")
  plt.xscale("log")
  plt.xlabel("M/[M]")
  plt.ylabel("f(M/[M])")

  sim = plt.scatter(frac_of_votes_sim, density_sim, edgecolors="#45ADA8", alpha = 0.8,facecolors='none')
  real = plt.scatter(frac_of_votes, density, edgecolors="red", alpha = 0.5,facecolors='none')

  plt.legend((sim, real),("Simulated", "Real"))

  return plt

def plot_s_margin(df, simulated_s_margin):
  # do the process for sim_margin first
  norm_sim_s_margin = simulated_s_margin/np.mean(simulated_s_margin)

  bin_values = np.histogram_bin_edges(norm_sim_s_margin, bins= 'scott')
  bin_values = sorted(bin_values)[1:]
  h = bin_values[1] - bin_values[0]

  # making a column called bin category
  bin_category = []

  for i in range(len(norm_sim_s_margin)):
    vote_share = norm_sim_s_margin[i]
    for j in range(len(bin_values)):
      if vote_share <= bin_values[j]:
        category_bin = bin_values[j]
        break
    bin_category.append(category_bin)

  # creating data for plotting log log plot
  frac_of_votes_sim_s = []
  density_sim_s = []
  unique_fractions = sorted(list(set(bin_category)))

  for i in range(len(unique_fractions)):
    frac_of_vote = unique_fractions[i] - (h/2)
    # get frequency per interval
    freq = bin_category.count(unique_fractions[i])
    rho = freq/len(bin_category)

    # update variables
    frac_of_votes_sim_s.append(frac_of_vote)
    density_sim_s.append(rho)
  
  # for the actual data
  df['S_Margin'] = df['Margin']/df['Turnout']

  # making plot for margin distribution
  s_margin = df['S_Margin'].tolist()

  norm_s_margin = s_margin/np.mean(s_margin)
  max_value = max(norm_s_margin)

  bin_values = np.histogram_bin_edges(norm_sim_s_margin, bins= 'scott')
  bin_values = sorted(bin_values)[1:]
  h = bin_values[1] - bin_values[0]

  # making a column called bin category
  bin_category = []

  for i in range(len(norm_s_margin)):
    vote_share = norm_s_margin[i]
    for j in range(len(bin_values)):
      if vote_share <= bin_values[j]:
        category_bin = bin_values[j]
        break
    bin_category.append(category_bin)

  # creating data for plotting log log plot
  frac_of_votes_s = []
  density_s = []
  unique_fractions = sorted(list(set(bin_category)))

  for i in range(len(unique_fractions)):
    frac_of_vote = unique_fractions[i] - (h/2)
    # get frequency per interval
    freq = bin_category.count(unique_fractions[i])
    rho = freq/len(bin_category)

    # update variables
    frac_of_votes_s.append(frac_of_vote)
    density_s.append(rho)

  # make the plots
  plt.figure(11)
  plt.title('Distribution of Normalized Specific Margin')
  plt.yscale("log")
  plt.xscale("log")
  plt.xlabel("S/[S]")
  plt.ylabel("f(S/[S])")

  sim = plt.scatter(frac_of_votes_sim_s, density_sim_s, edgecolors="#45ADA8", alpha = 0.8,facecolors='none')
  real = plt.scatter(frac_of_votes_s, density_s, edgecolors="red", alpha = 0.5,facecolors='none')

  plt.legend((sim, real),("Simulated", "Real"))

  return plt


