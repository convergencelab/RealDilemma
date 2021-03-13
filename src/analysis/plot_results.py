"""
Analysis of outcomes:

1. lets look at the difference between the algos for all three Qs

Measure agreement
Because the data is not normally distributed we will perform a kruskal-wallis test to see if there are any relationships
between the different samples
"""
import glob
import os
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()

DATA_DIR = r"C:\Users\NoahB\Desktop\School\fourth year (2020-2021)\ROBOTHESIS\RealDilemma\RealDilemma\src\analysis\data"
ALPHA = 0.05

def kruskal_wallis_and_plots(labels, total):
    algo_wise = pd.DataFrame(columns=["Algorithm", "Q1", "Q2", "Q3"])
    Qs = {}
    Qs["Q1"] = []
    Qs["Q2"] = []
    Qs["Q3"] = []
    indexes = {}
    for i, l in enumerate(labels):
        indexes[i] = l # in case we need to keep track of qs in list
        # store each question together
        Qs["Q1"].append(list(total.loc[l][1]))
        Qs["Q2"].append(list(total.loc[l][2]))
        Qs["Q3"].append(list(total.loc[l][3]))

    print("ALGO-WISE KRUSKAL WALLIS")
    for k in Qs.keys():
        print(f"{k} kruskal wallis test:")
        p, s = stats.kruskal(*Qs[k])
        if p > ALPHA:
            print('Same distributions (fail to reject H0)')
        else:
            print('Different distributions (reject H0)')

    print("QUESTION-WISE KRUSKAL WALLIS")
    Qs = [total.loc[:, 1],
          total.loc[:, 2],
          total.loc[:, 3]]
    p, s = stats.kruskal(*Qs)
    if p > ALPHA:
        print('Same distributions (fail to reject H0)')
    else:
        print('Different distributions (reject H0)')

    # sns.displot(total, x=1, hue="Algorithm", col="Algorithm", multiple="dodge")
    sns.displot(total, x=1, hue="Algorithm", element="step")
    sns.displot(total, x=2, hue="Algorithm", element="step")
    sns.displot(total, x=3, hue="Algorithm", element="step")
    # Kernel Density Estimation
    sns.displot(total, x=1, kind="kde")
    sns.displot(total, x=2, kind="kde")
    sns.displot(total, x=3, kind="kde")
    plt.show()
    tables = []
    for l in labels:
        tables.append(total.loc[l].describe().to_latex())

    with open(r"C:\Users\NoahB\Desktop\School\fourth year (2020-2021)\ROBOTHESIS\RealDilemma\RealDilemma\outputs\tables.txt", "w") as f:
        for t in tables:
            f.write(t)

def get_data():
    # load all data into pd dfs
    f = DATA_DIR + "\*"
    data_files = glob.glob(f)
    dfs = {}
    for f in data_files:
        k = os.path.basename(f).split(".")[0]
        df = pd.read_csv(f)
        df.columns = [0, 1, 2, 3]
        df = df.drop(0, axis=1)
        df = df.dropna()
        dfs[os.path.basename(f).split(".")[0]] = df  # keep track of each algorithm name in storing data
    # combine dfs based on the three qs
    # ALGO-WISE #
    total = pd.concat(dfs)
    total["Algorithm"] = [t[0] for t in total.index]
    labels = dfs.keys()
    return total, labels

def violins(total, labels):
    # get rid of outer level
    total.index = total.index.droplevel()
    # Q1, Q2, Q3 as x , and the question outcomes on the y, we will then have learning versus not learning
    # hue = learning vs not learning
    # x = Question
    # y = outcome
    # lets do A1 first
    Q1 = total.drop(2, axis=1).drop(3, axis=1)
    Q2 = total.drop(1, axis=1).drop(3, axis=1)
    Q3 = total.drop(1, axis=1).drop(2, axis=1)
    Q1["Question"] = ["Q1" for _ in range(len(Q1))]
    Q2["Question"] = ["Q2" for _ in range(len(Q2))]
    Q3["Question"] = ["Q3" for _ in range(len(Q3))]
    Q1 = Q1.rename(columns={i: "Response" for i in [1,2,3]})
    Q2 = Q2.rename(columns={i: "Response" for i in [1, 2, 3]})
    Q3 = Q3.rename(columns={i: "Response" for i in [1, 2, 3]})
    all_qs = Q1.append(Q2).append(Q3)
    algo1 = all_qs[(all_qs['Algorithm'].isin(["A1", "A1L"]))]
    algo2 = all_qs[(all_qs['Algorithm'].isin(["A2", "A2L"]))]
    fig, ax = plt.subplots(1,2, figsize=(10,5))
    fig.suptitle("Learning vs. Non-Learning")
    a1 = sns.violinplot(data=algo1, x="Question", y="Response", hue="Algorithm",
                    split=True, inner="quart", linewidth=1, ax=ax[0],legend_out = True
                    #palette={"Yes": "b", "No": ".85"}
                   )

    a2 = sns.violinplot(data=algo2, x="Question", y="Response", hue="Algorithm",
                   split=True, inner="quart", linewidth=1, ax=ax[1], legend_out = True
                   # palette={"Yes": "b", "No": ".85"}
                   )
    ax[0].set_title("PPO2")
    ax[1].set_title("A2C")
    plt.show()

    nonlearning = all_qs[(all_qs['Algorithm'].isin(["A1", "A2"]))]
    learning = all_qs[(all_qs['Algorithm'].isin(["A2L", "A1L"]))]

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("Policy vs. Learning")
    a3 = sns.violinplot(data=nonlearning, x="Question", y="Response", hue="Algorithm",
                        split=True, inner="quart", linewidth=1, ax=ax[0], legend_out=True
                        # palette={"Yes": "b", "No": ".85"}
                        )

    a4 = sns.violinplot(data=learning, x="Question", y="Response", hue="Algorithm",
                        split=True, inner="quart", linewidth=1, ax=ax[1], legend_out=True
                        # palette={"Yes": "b", "No": ".85"}
                        )
    ax[0].set_title("Policy")
    ax[1].set_title("Learning")
    plt.show()



if __name__ == "__main__":

    total, labels = get_data()
    # kruskal_wallis_and_plots(labels, total)
 #   violins(total, labels)












