# import libraries
from flask import Flask,render_template,jsonify
import pandas as pd


# create instance of Flask app
app = Flask(__name__)

# route for homeapge --------------------------------------------------------------------------------------------------
@app.route("/")
def homepage():
    
    #introduction for jumbotron
    title = "Belly Button Biodiversity"
    paragraph2="*******************************************************************************"
    paragraph3 ="The mission of this project was to investigate the microbes inhabiting our navels."
    paragraph4 = "Below is an interactive dashboard displaying some the results."
    paragraph = paragraph2 + "\n " +paragraph3 +" " + paragraph4


    return  render_template("index.html", title=title,paragraph= paragraph )


# route for namepage --------------------------------------------------------------------------------------------------
@app.route("/names")
def funcsampleName():
    
    # upload dataframe
    df_names= pd.read_csv('DataSets/belly_button_biodiversity_samples.csv')

    # created a list for sample id's
    nameList = []
    for each_name in df_names.columns[1:]:
        nameList.append(each_name)
   
    nameList = nameList
    return jsonify(nameList)


    
    return render_template("index.html" ,nameList = jsonify(nameList))


# route for otu --------------------------------------------------------------------------------------------------
@app.route("/otu")
def funcOtuDesc():

    # upload dataframe
    df_otuDesc = pd.read_csv("DataSets/belly_button_biodiversity_otu_id.csv")

    # created a list for the taxonomic units found
    otuDescList = []
    for each_otuDesc in df_otuDesc['lowest_taxonomic_unit_found']:
        otuDescList.append(each_otuDesc)
        
    return jsonify(otuDescList)


    return render_template("index.html", otu_nameList =  jsonify(otuDescList))


# route for meta/sample --------------------------------------------------------------------------------------------------
@app.route("/meta/sample")
def funcSampleMetaData():
    # upload dataframe
    df_sampleMetaData = pd.read_csv("DataSets/Belly_Button_Biodiversity_Metadata.csv")

    #added BB_ to the column sampleid
    df_sampleMetaData["SAMPLEID"]="BB_" + df_sampleMetaData["SAMPLEID"].astype(str)

    # selected need columns 
    df_sampleMetaData = df_sampleMetaData[['AGE','BBTYPE','ETHNICITY','GENDER','LOCATION','SAMPLEID']]

    # change df to json although python will return this as a string
    df_sampleMetaData_JSON = df_sampleMetaData.to_json(orient='records')
    
    return df_sampleMetaData_JSON


    return render_template('index.html', metaSampleProfile = jsonify(df_sampleMetaData_JSON))


## route for weekly frequency --------------------------------------------------------------------------------------------------
@app.route("/wfreq/sample")
def funcSampleMetaDataWFREQ():
    # upload dataframe
    df_sampleMetaData = pd.read_csv("DataSets/Belly_Button_Biodiversity_Metadata.csv")
    
    #added BB_ to the column sampleid
    df_sampleMetaData['SAMPLEID'] = "BB_" + df_sampleMetaData["SAMPLEID"].astype(str)
    
    # selected needed columns
    df_sampleMetaDataWFREQ = df_sampleMetaData[['SAMPLEID','WFREQ']]
    
    #filled na values with 0
    df_sampleMetaDataWFREQ = df_sampleMetaDataWFREQ.fillna(0) 
    
    #changed weekly frequency dataframe to json although python will return this as a string
    df_sampleMetaDataWFREQ = df_sampleMetaDataWFREQ.to_json(orient='records')
    
    
    return df_sampleMetaDataWFREQ


    return render_template('index.html', metaSampleNamesWFREQ = jsonify(df_sampleMetaDataWFREQ))

## route for pie and bubble plot --------------------------------------------------------------------------------------------------
@app.route("/sample/plot/pie") 
def funcDictSortedSampleValues():
    # upload dataframe
    df_Biodiversity = pd.read_csv('DataSets/belly_button_biodiversity_samples.csv')
    df_otu = pd.read_csv("DataSets/belly_button_biodiversity_otu_id.csv")
    # merge dataframe
    df_Biodiversity_merge = df_Biodiversity.merge(df_otu, on=['otu_id'],how='outer')
    # sum columns
    df_Biodiversity_merge["Total"] = df_Biodiversity_merge.iloc[::,1:].sum(axis=1)
    df_Biodiversity_sorted=df_Biodiversity_merge[['otu_id','lowest_taxonomic_unit_found', 'Total']]
    # sort and display top five
    df_Biodiversity_sorted = df_Biodiversity_sorted.sort_values(by=['Total'],ascending=False).head(10)
    return df_Biodiversity_sorted.to_json(orient='records')
    
    samplePIECHART = funcDictSortedSampleValues()


    return render_template("index.html", samplePIE = jsonify(samplePIECHART))


if __name__ == "__main__":
    app.run(debug=True)


