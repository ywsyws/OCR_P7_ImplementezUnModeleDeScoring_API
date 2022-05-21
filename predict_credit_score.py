import json
import joblib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import seaborn as sns
import shap


class Create_Figure:
    def __init__(self):
        # import model, data, explainer and feature names
        self.model = joblib.load("model/rf_classweight_na.pkl")
        self.X_test = np.load("data/X_test_transformed.npy")
        self.explainer = joblib.load(filename="model/explainer.bz2")
        with open("data/columns_list.json", "r") as f:
            columns_test = json.load(f)
        self.feature_names = columns_test
        self.shap_values = np.load("data/shap_value.npy")
        self.test_df = pd.read_csv("data/test_df.csv")
        self.X_test_df = pd.read_csv("data/X_test_3000.csv")

    def create_plotly(self, id: int):

        # predict credit score
        score = self.model[-1].predict_proba(self.X_test[id].reshape(1, -1))[0, 1]
        # plot guage chart
        fig = go.Figure(
            go.Indicator(
                domain={"x": [0, 1], "y": [0, 1]},
                value=score,
                mode="gauge+number+delta",
                title={"text": "Credit Score", "font": {"size": 70}},
                delta={
                    "reference": 0.47,
                    "increasing": {"color": "indianred"},
                    "decreasing": {"color": "green"},
                },
                gauge={
                    "axis": {"range": [None, 1]},
                    "steps": [
                        {"range": [0, 0.47], "color": "lightgreen"},
                        {"range": [0.47, 1], "color": "indianred"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 0.45,
                    },
                },
            )
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder), score

    def create_shap_force(self, id: int):
        shap.force_plot(
            self.explainer.expected_value[0],
            self.shap_values[id],
            feature_names=self.feature_names,
            out_names="Shap Value",
            matplotlib=True,
            show=False,
        )
        plt.savefig("static/images/force.png", bbox_inches="tight")
        plt.close()

    def create_shap_bar(self, id: int):
        shap.bar_plot(
            self.shap_values[id],
            max_display=18,
            feature_names=self.feature_names,
            show=False,
        )
        plt.savefig("static/images/bar.png", bbox_inches="tight")
        plt.close()

    def create_shap_waterfall(self, id: int):
        shap.plots._waterfall.waterfall_legacy(
            self.explainer.expected_value[0],
            self.shap_values[id],
            max_display=20,
            feature_names=self.feature_names,
        )
        plt.savefig("static/images/waterfall.png", bbox_inches="tight")
        plt.close()

    def create_shap_summary(self):
        shap.summary_plot(
            self.shap_values,
            features=self.X_test,
            feature_names=self.feature_names,
            alpha=0.05,
            show=False,
        )
        plt.savefig("static/images/summary.png", bbox_inches="tight")
        plt.close()

    def create_shap_dependence(self, feature_importance: str, index: int):
        shap.dependence_plot(
            feature_importance.index[index],
            self.shap_values,
            features=self.X_test,
            feature_names=self.feature_names,
            alpha=0.3,
            show=False,
        )
        plt.savefig("static/images/dependence.png", bbox_inches="tight")
        plt.close()

    def create_scatter(self, id: int, scatter_x: str, scatter_y: str):
        hue = "TARGET"
        sns.scatterplot(x=scatter_x, y=scatter_y, data=self.test_df, hue=hue)
        ax = sns.scatterplot(
            x=scatter_x,
            y=scatter_y,
            data=self.test_df[id : id + 1],
            hue=hue,
            palette=["red"],
        )
        plt.title(f"{scatter_y} vs. {scatter_x}", fontdict={"fontsize": 18})
        legend_labels, _ = ax.get_legend_handles_labels()
        ax.legend(legend_labels, ["Approved", "Not Approved", "YOU"])
        plt.savefig("static/images/scatter.png", bbox_inches="tight")
        plt.close()

    def create_bullet_guage_amt_credit(self, id: int):
        amt_credit = self.X_test_df.AMT_CREDIT
        fig = go.Figure(
            go.Indicator(
                mode="number+gauge+delta",
                gauge={
                    "shape": "bullet",
                    "axis": {"range": [amt_credit.min(), amt_credit.max()]},
                    "threshold": {
                        "line": {"color": "red", "width": 2},
                        "thickness": 0.75,
                        "value": amt_credit.median(),
                    },
                },
                value=amt_credit[id],
                delta={"reference": amt_credit.median()},
                domain={"x": [0.1, 1], "y": [0, 1]},
                title={"text": "Credit Amount"},
            )
        )
        fig.update_layout(height=250)

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    def create_bullet_guage_amt_income(self, id: int):
        amt_income_total = self.X_test_df.AMT_INCOME_TOTAL
        fig = go.Figure(
            go.Indicator(
                mode="number+gauge+delta",
                gauge={
                    "shape": "bullet",
                    "axis": {"range": [amt_income_total.min(), amt_income_total.max()]},
                    "threshold": {
                        "line": {"color": "red", "width": 2},
                        "thickness": 0.75,
                        "value": amt_income_total.median(),
                    },
                },
                value=amt_income_total[id],
                delta={"reference": amt_income_total.median()},
                domain={"x": [0.1, 1], "y": [0, 1]},
                title={"text": "Total Income"},
            )
        )
        fig.update_layout(height=250)

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
