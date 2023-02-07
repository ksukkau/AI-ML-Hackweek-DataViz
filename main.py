import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def read_data(filename):
    # load data
    data = pd.read_csv(filename)
    # remove any rows that contain 'nan'
    data.dropna(axis=0, how='any', inplace=True)

    return data


def create_line_plot(fx, fy, mx, my):
    N = 10
    plt.title('Gender Pay Gap')
    plt.xlabel("Job title")
    plt.ylabel(" Average Pay")
    plt.plot(fx, fy, color='green', label="Female")
    plt.plot(mx, my, color='red', label="Male")
    plt.legend(loc="upper left")
    plt.gca().margins(x=0)
    plt.gcf().canvas.draw()
    tl = plt.gca().get_xticklabels()
    maxsize = max([t.get_window_extent().width for t in tl])
    m = 0.2  # inch margin
    s = maxsize / plt.gcf().dpi * N + 2 * m
    margin = m / plt.gcf().get_size_inches()[0]

    plt.gcf().subplots_adjust(left=margin, right=1. - margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])
    plt.show()


def create_barchart(womens_jobs, mens_jobs, job_titles):

    X_axis = np.arange(len(job_titles))
    plt.figure(figsize=(20, 3))
    plt.bar(X_axis - 0.2, womens_jobs, 0.4, label='Women')
    plt.bar(X_axis + 0.2, mens_jobs, 0.4, label='Men')
    plt.xticks(X_axis, job_titles)
    plt.xlabel("Titles")
    plt.ylabel("Count")
    plt.title("Ratio of women to Men by Job title")

    plt.legend()
    plt.show()


def split_data_by_gender(data):
    data_female = data[data['Gender'] == 'Female']
    data_male = data[data['Gender'] == 'Male']
    women_vs_men_by_title(data_female, data_male)
    return data_female, data_male


def total_pay(data_female, data_male):
    data_female['TotalPay'] = data_female['BasePay'] + data_female['Bonus']
    data_male['TotalPay'] = data_male['BasePay'] + data_male['Bonus']
    return data_female, data_male


def process_data(data):
    data_female, data_male = split_data_by_gender(data)
    data_female, data_male = total_pay(data_female, data_male)
    return data_female, data_male


def make_graph_pay_on_title(data_female, data_male):
    data_female = data_female.sort_values(by='JobTitle', axis=0)
    data_male = data_male.sort_values(by='JobTitle', axis=0)
    fy = data_female.groupby('JobTitle')['TotalPay'].mean()
    fx = data_female['JobTitle'].unique()
    my = data_male.groupby('JobTitle')['TotalPay'].mean()
    mx = data_male['JobTitle'].unique()
    create_line_plot(fx, fy, mx, my)


def women_vs_men_by_title(data_female, data_male):
    job_titles = data_female['JobTitle'].unique()
    mens_jobs = data_male.groupby('JobTitle')['Gender'].count()
    womens_jobs = data_female.groupby('JobTitle')['Gender'].count()
    create_barchart(womens_jobs, mens_jobs, job_titles)


if __name__ == '__main__':
    data = read_data("Glassdoor_Gender_Pay_Gap.csv")
    data_female, data_male = process_data(data)
    make_graph_pay_on_title(data_female, data_male)
