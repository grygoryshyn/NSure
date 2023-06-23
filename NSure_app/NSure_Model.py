# Installing necessary Libraries, Packages, and Functions
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle as pkl

# Creating the flask app to establish a connection between the HTML and the python model code
flask_app = Flask(__name__)

# Loading in the stored classification model found in the 'Model Development' folder of this repository
NSure_model = pkl.load(open("model.pkl", "rb"))


# Defining a Flask route for the root URL of the web application
@flask_app.route("/")
def home():
    """
    Loading homepage HTML
    """

    return render_template("home.html")


@flask_app.route("/predict", methods=["POST"])
def predict():
    """
    Defining Processing and Rendering logic for to tranform the
    input data sent by the html forms into formatted array values
    to create predictions for display on the HTML GUI
    """

    # obtaining predicted values through form request sent to NSure_model and formatting them to work with the model's format
    init_values = [x for x in request.form.values()]
    raw_values = np.array(init_values)
    def_vals = np.array(
        [60, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )  # creating default input value array following the correct model format

    # assigning the 'NC_reimbursement' feature values
    def_vals[0] = raw_values[3]

    # formatting the 'CPM' feature values
    def_vals[1] = raw_values[0]

    # assigning and formatting the 'P_term' dummy feature values
    def_vals[0] = raw_values[3]
    if raw_values[1] == "0":
        def_vals[2] = 1
    if raw_values[1] == "1":
        def_vals[3] = 1
    if raw_values[1] == "2":
        def_vals[4] = 1
    if raw_values[1] == "3":
        def_vals[5] = 1

    # assigning and formatting the 'Healthcare_cover' dummy feature values
    if raw_values[2] == "0":
        def_vals[6] = 1
    if raw_values[2] == "1":
        def_vals[7] = 1
    if raw_values[2] == "2":
        def_vals[8] = 1

    # assigning and formatting the 'Bundle_options' dummy feature values
    if raw_values[4] == "0":
        def_vals[9] = 1
    if raw_values[4] == "1":
        def_vals[10] = 1
    if raw_values[4] == "2":
        def_vals[11] = 1

    # assigning and formatting the 'Dental_options' dummy feature values
    if raw_values[5] == "0":
        def_vals[12] = 1
    if raw_values[5] == "1":
        def_vals[13] = 1

    # assigning and formatting the 'Physio_term' dummy feature values
    if raw_values[6] == "0":
        def_vals[14] = 1
    if raw_values[6] == "1":
        def_vals[15] = 1

    # assigning and formatting the 'Mental_health_options' dummy feature values
    if raw_values[7] == "0":
        def_vals[16] = 1
    if raw_values[7] == "1":
        def_vals[17] = 1

    # assigning and formatting the 'International_cover' dummy feature values
    if raw_values[8] == "0":
        def_vals[18] = 1
    if raw_values[8] == "1":
        def_vals[19] = 1

    input_values = [def_vals.astype(float)]  # converting all values into float type
    probs = NSure_model.predict_proba(
        input_values
    )  # creating prediction for probabilities of reccommending different insurance plans

    top_3 = np.argsort(probs)[
        :, : -3 - 1 : -1
    ]  # Taking the top 3 ranked most probable insurance policies
    top_probs = np.sort(probs)[
        :, : -3 - 1 : -1
    ]  # Taking the top probabilities of the 3 ranked most probable insurance policies

    ins_1 = top_3[0][
        0
    ]  # storing the name of the first placed reccommended insurance plan policy
    pro_1 = top_probs[0][
        0
    ]  # storing the probability of the first placed reccommended insurance plan policy

    ins_2 = top_3[0][
        1
    ]  # storing the name of the second placed reccommended insurance plan policy
    pro_2 = top_probs[0][
        1
    ]  # storing the probability of the second placed reccommended insurance plan policy

    ins_3 = top_3[0][
        2
    ]  # storing the name of the third placed reccommended insurance plan policy
    pro_3 = top_probs[0][
        2
    ]  # storing the probability of the third placed reccommended insurance plan policy

    match_score_1 = round(
        (pro_1 / (pro_1 + pro_2 + pro_3)) * 100, 2
    )  # calculating the 'Matching Score' of the first ranked insurance policy relative to the top 3 ranked policies
    match_score_2 = round(
        (pro_2 / (pro_1 + pro_2 + pro_3)) * 100, 2
    )  # calculating the 'Matching Score' of the second ranked insurance policy relative to the top 3 ranked policies
    match_score_3 = round(
        (pro_3 / (pro_1 + pro_2 + pro_3)) * 100, 2
    )  # calculating the 'Matching Score' of the third ranked insurance policy relative to the top 3 ranked policies

    # defining list with all insurance policies
    insurances = [
        "FTBO Base Free",
        "FTBO Basic",
        "FTBO Basis Plus",
        "ONVZ basic health-care plan",
        "United Customers: Basic Choice",
        "United Customers: Conscious Choice",
        "United Customers: Own Choice",
        "United Customers: Wide Choice",
        "Unive Arranged Care",
        "Unive Basic Care",
        "Unive Free Care",
        "Unive Select Care",
        "VGZ Basic Choice",
        "VGZ Own Choice",
        "VGZ Wide Choice",
        "Zilveren Kruis: Basic Budget",
        "Zilveren Kruis: Basic Exclusive",
        "Zilveren Kruis: Basic Sure",
    ]

    # providing links to the top three predicted insurances
    first_link = ""
    if insurances[ins_1] == "FTBO Base Free":
        first_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis-vrij"
    if insurances[ins_1] == "FTBO Basic":
        first_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis"
    if insurances[ins_1] == "FTBO Basis Plus":
        first_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis-plus"

    if insurances[ins_1] == "United Customers: Basic Choice":
        first_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-basis-keuze.jsp"
    if insurances[ins_1] == "United Customers: Conscious Choice":
        first_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-bewuste-keuze.jsp"
    if insurances[ins_1] == "United Customers: Own Choice":
        first_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-eigen-keuze.jsp"
    if insurances[ins_1] == "United Customers: Wide Choice":
        first_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-ruime-keuze.jsp"

    if insurances[ins_1] == "ONVZ basic health-care plan":
        first_link = "https://www.onvz.nl/en/health-insurances/basic-health-care-plan"

    if insurances[ins_1] == "Unive Arranged Care":
        first_link = "https://www.unive.nl/zorgverzekering/basisverzekering/geregeld"
    if insurances[ins_1] == "Unive Basic Care":
        first_link = "https://www.unive.nl/zorgverzekering/basisverzekering/basis"
    if insurances[ins_1] == "Unive Free Care":
        first_link = "https://www.unive.nl/zorgverzekering/basisverzekering/vrij"
    if insurances[ins_1] == "Unive Select Care":
        first_link = "https://www.unive.nl/zorgverzekering/basisverzekering/select"

    if insurances[ins_1] == "VGZ Basic Choice":
        first_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/basis-keuze"
    if insurances[ins_1] == "VGZ Own Choice":
        first_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/eigen-keuze"
    if insurances[ins_1] == "VGZ Wide Choice":
        first_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/ruime-keuze"

    if insurances[ins_1] == "Zilveren Kruis: Basic Budget":
        first_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-budget"
    if insurances[ins_1] == "Zilveren Kruis: Basic Exclusive":
        first_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-exclusief"
    if insurances[ins_1] == "Zilveren Kruis: Basic Sure":
        first_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-zeker"

    second_link = ""
    if insurances[ins_2] == "FTBO Base Free":
        second_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis-vrij"
    if insurances[ins_2] == "FTBO Basic":
        second_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis"
    if insurances[ins_2] == "FTBO Basis Plus":
        second_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis-plus"

    if insurances[ins_2] == "United Customers: Basic Choice":
        second_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-basis-keuze.jsp"
    if insurances[ins_2] == "United Customers: Conscious Choice":
        second_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-bewuste-keuze.jsp"
    if insurances[ins_2] == "United Customers: Own Choice":
        second_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-eigen-keuze.jsp"
    if insurances[ins_2] == "United Customers: Wide Choice":
        second_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-ruime-keuze.jsp"

    if insurances[ins_2] == "ONVZ basic health-care plan":
        second_link = "https://www.onvz.nl/en/health-insurances/basic-health-care-plan"

    if insurances[ins_2] == "Unive Arranged Care":
        second_link = "https://www.unive.nl/zorgverzekering/basisverzekering/geregeld"
    if insurances[ins_2] == "Unive Basic Care":
        second_link = "https://www.unive.nl/zorgverzekering/basisverzekering/basis"
    if insurances[ins_2] == "Unive Free Care":
        second_link = "https://www.unive.nl/zorgverzekering/basisverzekering/vrij"
    if insurances[ins_2] == "Unive Select Care":
        second_link = "https://www.unive.nl/zorgverzekering/basisverzekering/select"

    if insurances[ins_2] == "VGZ Basic Choice":
        second_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/basis-keuze"
    if insurances[ins_2] == "VGZ Own Choice":
        second_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/eigen-keuze"
    if insurances[ins_2] == "VGZ Wide Choice":
        second_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/ruime-keuze"

    if insurances[ins_2] == "Zilveren Kruis: Basic Budget":
        second_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-budget"
    if insurances[ins_2] == "Zilveren Kruis: Basic Exclusive":
        second_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-exclusief"
    if insurances[ins_2] == "Zilveren Kruis: Basic Sure":
        second_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-zeker"

    third_link = ""
    if insurances[ins_3] == "FTBO Base Free":
        third_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis-vrij"
    if insurances[ins_3] == "FTBO Basic":
        third_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis"
    if insurances[ins_3] == "FTBO Basis Plus":
        third_link = "https://www.fbto.nl/zorgverzekering/basisverzekering/basis-plus"

    if insurances[ins_3] == "United Customers: Basic Choice":
        third_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-basis-keuze.jsp"
    if insurances[ins_3] == "United Customers: Conscious Choice":
        third_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-bewuste-keuze.jsp"
    if insurances[ins_3] == "United Customers: Own Choice":
        third_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-eigen-keuze.jsp"
    if insurances[ins_3] == "United Customers: Wide Choice":
        third_link = "https://www.unitedconsumers.com/zorgverzekering/basisverzekering/uc-ruime-keuze.jsp"

    if insurances[ins_3] == "ONVZ basic health-care plan":
        third_link = "https://www.onvz.nl/en/health-insurances/basic-health-care-plan"

    if insurances[ins_3] == "Unive Arranged Care":
        third_link = "https://www.unive.nl/zorgverzekering/basisverzekering/geregeld"
    if insurances[ins_3] == "Unive Basic Care":
        third_link = "https://www.unive.nl/zorgverzekering/basisverzekering/basis"
    if insurances[ins_3] == "Unive Free Care":
        third_link = "https://www.unive.nl/zorgverzekering/basisverzekering/vrij"
    if insurances[ins_3] == "Unive Select Care":
        third_link = "https://www.unive.nl/zorgverzekering/basisverzekering/select"

    if insurances[ins_3] == "VGZ Basic Choice":
        third_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/basis-keuze"
    if insurances[ins_3] == "VGZ Own Choice":
        third_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/eigen-keuze"
    if insurances[ins_3] == "VGZ Wide Choice":
        third_link = "https://www.vgz.nl/zorgverzekering/basisverzekering/ruime-keuze"

    if insurances[ins_3] == "Zilveren Kruis: Basic Budget":
        third_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-budget"
    if insurances[ins_3] == "Zilveren Kruis: Basic Exclusive":
        third_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-exclusief"
    if insurances[ins_3] == "Zilveren Kruis: Basic Sure":
        third_link = "https://www.zilverenkruis.nl/consumenten/zorgverzekering/basisverzekering/basis-zeker"

    # returning values calculated using the ML model back to the HTML website
    return render_template(
        "home.html",
        predicted_first_insurance="{}".format(insurances[ins_1]),
        predicted_first_insurance_link="{}".format(first_link),
        predicted_second_insurance="{}".format(insurances[ins_2]),
        predicted_second_insurance_link="{}".format(second_link),
        predicted_third_insurance="{}".format(insurances[ins_3]),
        predicted_third_insurance_link="{}".format(third_link),
        match_score_first_insurance="{}".format(match_score_1),
        match_score_second_insurance="{}".format(match_score_2),
        match_score_third_insurance="{}".format(match_score_3),
    )

# Enabling debug functionality during development of the web application
if __name__ == "__main__":
    flask_app.run(debug=True)