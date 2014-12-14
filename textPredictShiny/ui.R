
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)

shinyUI(pageWithSidebar(
                headerPanel("",
                            tags$head(
                                    tags$img(src="header.png", height="150px", width = 1200)
                            )
                ),
                sidebarPanel(
                        h5('Instructions:'),
                        helpText("Enter your text in the textarea on the right side."),
                        helpText("Enter a space (' ') and wait for a while(1-2 sec.) for next word prediction."),
                        helpText("If you are copying a phrase with trailing space or removed all text in input textarea, please enter an extra space for prediction."),
                        helpText("Top Prediction appears at top, and top 3 appear below the input textarea."),
                        helpText("Press escape key ('Esc') to append the top predicted word in the input textarea."),
                        helpText("If having problem like inactivity or gray page, please refresh several times or change browser.")
                        
                ),
                mainPanel(     
                                           
                        fluidPage(
                                fluidRow(
                                        column(3, 
                                               h5('Top Prediction:'),
                                               # using input instead of output for resulted prediction, 
                                               # so that we can control the value from server.R 
                                               textInput("textPredict1", "", "The"),
                                               # as this input text box will hold result, better disable it
                                               tags$script('
                                                        document.getElementById("textPredict1").disabled = true;
                                               '),
                                               tags$head(tags$style("#textPredict1{color: red;font-size: 20px;font-style: italic; }"))
                                        )
                                ),
                                fluidRow(
                                        column(9, 
                                               h5('Enter your texts:'),
                                               tags$textarea(id="inputString", class="comments", rows="10", cols="200", 
                                                             placeholder="Enter your text here.", ""),
                                               tags$style(HTML(".comments { width: 500px; height: 200px }")),
                                               
                                               # java script to collect key stroke
                                               # Shiny.onInputChange sends the key stroke as inout variable
                                               tags$script('
                                                    $(document).on("keydown", function (e) {
                                                        Shiny.onInputChange("keydata", e.which);
                                                    });      
                                                ') 
                                        )
                                        
                                ),
                                fluidRow(
                                        column(3, 
                                               h5('3 Top Predictions:'),
                                               textOutput("textPredict1of3"),
                                               textOutput("textPredict2of3"),
                                               textOutput("textPredict3of3")
                                        )
                                )
                                                                        
                        )
                        
                )
        )
)