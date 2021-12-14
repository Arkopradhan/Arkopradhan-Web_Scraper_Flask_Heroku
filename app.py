# doing necessary imports

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString # preparing the URL to search the product on flipkart
            uClient = uReq(flipkart_url) # requesting the webpage from the internet
            flipkartPage = uClient.read() # reading the webpage
            uClient.close() # closing the connection to the web server
            flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
            bigboxes = flipkart_html.findAll("div", {"class": "_2kHMtA"}) # seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0] #  taking the first iteration (for demo)
            productLink = "https://www.flipkart.com" + box.a['href'] # extracting the actual product link
            prodRes = requests.get(productLink) # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {'class': "col _2wzgFH"}) # finding the HTML section containing the customer comments
            i=0
            comment_boxes_name = prod_html.find_all('div', {'class': "row _3n8db9"})
            comment_boxes_comments = prod_html.find_all('div', {'class': "t-ZTKy"})

            reviews = [] # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for commentbox in commentboxes:
                try:
                    rating = str(commentbox.div.text)[0]
                except:
                    rating = 'No Rating'

                try:
                    commentHead = str(commentbox.div.text)[1:]
                except:
                    commentHead = 'No Comment Heading'

    
                try:
                    comment_boxes_name0 = comment_boxes_name[i]
                    ww = comment_boxes_name0
                    name = ww.div.p.text
                    name = name.title()

                except:
                    name = 'No Name'

                try:
                    comment_boxes_comments_ = comment_boxes_comments[i]
                    ww = comment_boxes_comments_
                    custComment = ww.div.div.text
                except:
                    custComment = 'No Customer Comment'
                i+=1
                #fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                              "Comment": custComment} # saving that detail to a dictionary
                #x = table.insert_one(mydict) #insertig the dictionary containing the rview comments to the collection
                reviews.append(mydict) #  appending the comments to the review list
            return render_template('results.html', reviews=reviews) # showing the review to the user
        except:
            return 'something is wrong'
            #return render_template('results.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000