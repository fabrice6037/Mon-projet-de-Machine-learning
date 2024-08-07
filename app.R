

library(shiny)
library(shinydashboard)

# Define UI for application that draws a histogram
ui <- dashboardPage(
   dashboardHeader(title="Prediction de la desactivation des entreprises",
                   titleWidth = 450),
   dashboardSidebar(
       sidebarMenu(
         menuItem("Accueil", tabName = "accueil", icon = icon("home")),
         menuItem("Téléchargement des données", tabName = "upload", icon = icon("upload")),
         menuItem("Sélection des modèles", tabName = "modeling", icon = icon("cogs")),
         menuItem("Prédiction", tabName = "prediction", icon = icon("chart-line"))
   )),
   dashboardBody(
     tabItems(
       # Page d'accueil
       tabItem(tabName = "accueil",
               fluidRow(
                 box(title = "Description du Projet", width = 12,
                     p("Ce projet a pour but de prédire la désactivation des entreprises du fichier de l’identifiant financier unique (IFU). Les variables explicatives incluent :"),
                     tags$ul(
                       tags$li("Âge de l’entreprise"),
                       tags$li("Secteur d’activité"),
                       tags$li("Nombre de déclarations par an"),
                       tags$li("Nombre d’impôts assujettis"),
                       tags$li("Présence d’exonération"),
                       tags$li("Nombre d’entreprises en concurrence"),
                       tags$li("Lieu de création"),
                       tags$li("Forme juridique"),
                       tags$li("Nombre de redressements subis"),
                       tags$li("Nombre de marchés publics")
                     )))),
    tabItem(tabName="prediction",
    fluidRow(box(valueBoxOutput("Scores de prediction")),
    box(numericInput("var1",label="Age de l'entreprise",value=20,min=10)),
    fluidRow(box(selectizeInput("var2",label="Secteur d'activité de l'entreprise",choices=c("privree","primaire")))),
    box(numericInput("var3",label=" Nombre de déclarations par an",value=0,min=10)))
  )
)
))

# Define server logic required to draw a histogram
server <- function(input, output) {
   
   prediction=reactive({
     predict(
       model,
       data.frame(
         "age_ent"=input$var1,
         "sect_act"=input$var2,
         "nbr_declare"=input$var3
       ),
       type="raw"
     )
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

