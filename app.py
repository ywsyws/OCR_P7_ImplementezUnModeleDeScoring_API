import pandas as pd
from flask import Flask, render_template, redirect, request, url_for

from predict_credit_score import Create_Figure
from forms import LoginForm

# Create the application instance
app = Flask(__name__, template_folder="templates")
app.config["WTF_CSRF_ENABLED"] = False
app.config["WTF_CSRF_CHECK_DEFAULT"] = False


create_figure = Create_Figure()


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home page of the credit score API.
    """
    # return "channing"
    form = LoginForm()
    if request.method == "POST":
        id = int(request.form["id"]) - 1
        return redirect(
            url_for(
                "detail",
                id=id,
                index=0,
                scatter_x="AMT_CREDIT",
                scatter_y="CNT_CHILDREN",
            )
        )
    return render_template("home/welcome.html", form=form)


@app.route("/<id>/<index>/<scatter_x>/<scatter_y>/detail", methods=["GET", "POST"])
def detail(id, index, scatter_x, scatter_y):
    """
    Show credit score of a client.
    """
    id = int(id)
    features_importance = pd.read_csv("data/feature_importance.csv", index_col=0)
    dependence_features = features_importance.index.to_list()
    dependence_features.remove("ORGANIZATION_TYPE_Advertising")
    if request.method == "POST":
        try:
            feature = request.form["dependence_features"]
            index = features_importance.index.to_list().index(feature)
            create_figure.create_shap_dependence(features_importance, index)
        except:
            pass
        try:
            scatter_y = request.form["scatter_features_y"]
            scatter_x = request.form["scatter_features_x"]
            create_figure.create_scatter(id, scatter_x, scatter_y)
        except:
            pass
        return redirect(
            url_for(
                "detail", id=id, index=index, scatter_x=scatter_x, scatter_y=scatter_y
            )
        )
    graphJSON, score = create_figure.create_plotly(id)
    create_figure.create_shap_force(id)
    create_figure.create_shap_bar(id)
    create_figure.create_shap_waterfall(id)
    create_figure.create_shap_summary()
    create_figure.create_shap_dependence(features_importance, int(index))
    create_figure.create_scatter(id, scatter_x, scatter_y)
    graphJSON_amt_credit = create_figure.create_bullet_guage_amt_credit(id)
    graphJSON_amt_income = create_figure.create_bullet_guage_amt_income(id)
    result = "Not Approved" if score >= 0.47 else "Approved"

    return render_template(
        "home/dashboard.html",
        id=id,
        index=index,
        dependence_features=dependence_features,
        scatter_features_x=features_importance.index,
        scatter_features_y=features_importance.index,
        graphJSON=graphJSON,
        graphJSON_amt_credit=graphJSON_amt_credit,
        graphJSON_amt_income=graphJSON_amt_income,
        result=result,
    )


# If we're running in stand alone mode, run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5030)
