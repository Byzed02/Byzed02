{
      "source": [
        "import pandas as pd\n",
        "import numpy as np\n",
        "import re\n",
        "import nltk\n",
        "from sklearn.feature_extraction.text import TfidfVectorizer\n",
        "from sklearn.metrics.pairwise import cosine_similarity\n",
        "import pickle\n",
        "import pandas as pd\n",
        "import streamlit as st\n",
        "from streamlit import session_state as session\n",
        "from flask import Flask, request, jsonify\n",
        "from flask_restful import Api, Resource\n",
        "\n",
        "app = Flask(__name__)\n",
        "api = Api(app)"
      ]
     
      cell_type: "code",
      "source": [
        "movies_df= pd.read_csv('movies.csv')\n",
        "ratings_df= pd.read_csv('ratings.csv')"
      ],
      "metadata": {
        "id": "0wYeMiKspiBv"
      },
      "execution_count": null,
      "outputs": []
    {
      "cell_type": "code",
      "source": [
        "# Copie du dataframedans un nouveau dataframe\n",
        "moviesWithGenres_df= movies_df.copy()"
      ],
      "metadata": {
        "id": "j3k6alU1olP7"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Pour chaque ligne du dataframe, parcourir la liste de genres et placer 1 à la colonne correspondante du nouveau dataframe\n",
        "for index, row in movies_df.iterrows():\n",
        "    for genre in row['genres']:\n",
        "        moviesWithGenres_df.at[index, genre] = 1"
      ],
      "metadata": {
        "id": "3uoHekFGpeFi"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Remplacer les valeurs NaNpar des 0 pour indiquer qu'un film n'est pas de ce genre\n",
        "moviesWithGenres_df= moviesWithGenres_df.fillna(0)\n",
        "moviesWithGenres_df.head()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 235
        },
        "id": "BDUWzYylsyD2",
        "outputId": "0153dcb7-a883-4203-e5ea-7bde64a4def2"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "   movieId                        title  \\\n",
              "0        1                    Toy Story   \n",
              "1        2                      Jumanji   \n",
              "2        3             Grumpier Old Men   \n",
              "3        4            Waiting to Exhale   \n",
              "4        5  Father of the Bride Part II   \n",
              "\n",
              "                                        genres    year    A    d    v    e  \\\n",
              "0  Adventure|Animation|Children|Comedy|Fantasy  1995.0  1.0  1.0  1.0  1.0   \n",
              "1                   Adventure|Children|Fantasy  1995.0  1.0  1.0  1.0  1.0   \n",
              "2                               Comedy|Romance  1995.0  0.0  1.0  0.0  1.0   \n",
              "3                         Comedy|Drama|Romance  1995.0  0.0  1.0  0.0  1.0   \n",
              "4                                       Comedy  1995.0  0.0  1.0  0.0  1.0   \n",
              "\n",
              "     n    t  ...    S    -    I    X    W    N    (         g    )  \n",
              "0  1.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  \n",
              "1  1.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  \n",
              "2  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  \n",
              "3  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  \n",
              "4  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  \n",
              "\n",
              "[5 rows x 39 columns]"
            ],
            "text/html": [
              "\n",
              "\n",
              "  <div id=\"df-12794de8-e77e-4082-986e-70bf5bbcab3a\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>movieId</th>\n",
              "      <th>title</th>\n",
              "      <th>genres</th>\n",
              "      <th>year</th>\n",
              "      <th>A</th>\n",
              "      <th>d</th>\n",
              "      <th>v</th>\n",
              "      <th>e</th>\n",
              "      <th>n</th>\n",
              "      <th>t</th>\n",
              "      <th>...</th>\n",
              "      <th>S</th>\n",
              "      <th>-</th>\n",
              "      <th>I</th>\n",
              "      <th>X</th>\n",
              "      <th>W</th>\n",
              "      <th>N</th>\n",
              "      <th>(</th>\n",
              "      <th></th>\n",
              "      <th>g</th>\n",
              "      <th>)</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>1</td>\n",
              "      <td>Toy Story</td>\n",
              "      <td>Adventure|Animation|Children|Comedy|Fantasy</td>\n",
              "      <td>1995.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>2</td>\n",
              "      <td>Jumanji</td>\n",
              "      <td>Adventure|Children|Fantasy</td>\n",
              "      <td>1995.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>3</td>\n",
              "      <td>Grumpier Old Men</td>\n",
              "      <td>Comedy|Romance</td>\n",
              "      <td>1995.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>4</td>\n",
              "      <td>Waiting to Exhale</td>\n",
              "      <td>Comedy|Drama|Romance</td>\n",
              "      <td>1995.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>5</td>\n",
              "      <td>Father of the Bride Part II</td>\n",
              "      <td>Comedy</td>\n",
              "      <td>1995.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>1.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>...</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "      <td>0.0</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "<p>5 rows × 39 columns</p>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-12794de8-e77e-4082-986e-70bf5bbcab3a')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "\n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "\n",
              "\n",
              "\n",
              "    <div id=\"df-9025c283-8c6f-4cf6-be0d-dd3ebfefa037\">\n",
              "      <button class=\"colab-df-quickchart\" onclick=\"quickchart('df-9025c283-8c6f-4cf6-be0d-dd3ebfefa037')\"\n",
              "              title=\"Suggest charts.\"\n",
              "              style=\"display:none;\">\n",
              "\n",
              "<svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "     width=\"24px\">\n",
              "    <g>\n",
              "        <path d=\"M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z\"/>\n",
              "    </g>\n",
              "</svg>\n",
              "      </button>\n",
              "    </div>\n",
              "\n",
              "<style>\n",
              "  .colab-df-quickchart {\n",
              "    background-color: #E8F0FE;\n",
              "    border: none;\n",
              "    border-radius: 50%;\n",
              "    cursor: pointer;\n",
              "    display: none;\n",
              "    fill: #1967D2;\n",
              "    height: 32px;\n",
              "    padding: 0 0 0 0;\n",
              "    width: 32px;\n",
              "  }\n",
              "\n",
              "  .colab-df-quickchart:hover {\n",
              "    background-color: #E2EBFA;\n",
              "    box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "    fill: #174EA6;\n",
              "  }\n",
              "\n",
              "  [theme=dark] .colab-df-quickchart {\n",
              "    background-color: #3B4455;\n",
              "    fill: #D2E3FC;\n",
              "  }\n",
              "\n",
              "  [theme=dark] .colab-df-quickchart:hover {\n",
              "    background-color: #434B5C;\n",
              "    box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "    filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "    fill: #FFFFFF;\n",
              "  }\n",
              "</style>\n",
              "\n",
              "    <script>\n",
              "      async function quickchart(key) {\n",
              "        const containerElement = document.querySelector('#' + key);\n",
              "        const charts = await google.colab.kernel.invokeFunction(\n",
              "            'suggestCharts', [key], {});\n",
              "      }\n",
              "    </script>\n",
              "\n",
              "      <script>\n",
              "\n",
              "function displayQuickchartButton(domScope) {\n",
              "  let quickchartButtonEl =\n",
              "    domScope.querySelector('#df-9025c283-8c6f-4cf6-be0d-dd3ebfefa037 button.colab-df-quickchart');\n",
              "  quickchartButtonEl.style.display =\n",
              "    google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "}\n",
              "\n",
              "        displayQuickchartButton(document);\n",
              "      </script>\n",
              "      <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-12794de8-e77e-4082-986e-70bf5bbcab3a button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-12794de8-e77e-4082-986e-70bf5bbcab3a');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n"
            ]
          },
          "metadata": {},
          "execution_count": 100
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# Supprimer une colonne ou une ligne spécifique d'un dataframe\n",
        "ratings_df= ratings_df.drop('timestamp',1)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "Kx_1Nnc6s3S3",
        "outputId": "d2740819-d649-4c54-eb57-292f38cea7b6"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "<ipython-input-101-51579fef6eff>:2: FutureWarning: In a future version of pandas all arguments of DataFrame.drop except for the argument 'labels' will be keyword-only.\n",
            "  ratings_df= ratings_df.drop('timestamp',1) ## donne de l'axe selon lequel\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def Movies_Recommandations(userInput, ratings_df, moviesWithGenres_df, n_recommandations=10):\n",
        "  #Les notes attribuées par l'utilisateur\n",
        "  inputMovies= pd.DataFrame(userInput)\n",
        "\n",
        "  #Filtrer les films sur la base des titres\n",
        "  inputId= movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]\n",
        "\n",
        "  #Fusionner de façon implicite sur la base des titre, pour avoir notre dataframe\n",
        "  inputMovies= pd.merge(inputId, inputMovies)\n",
        "\n",
        "  # Supprimer les colonnes dont nous n'avons pas besoin dans notre dataframepour libérer de la mémoire\n",
        "  inputMovies= inputMovies.drop('genres', 1).drop('year', 1)\n",
        "\n",
        "  # Filtrer les films\n",
        "  userMovies= moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]\n",
        "\n",
        "  # Réinitialisation de l'index\n",
        "  userMovies= userMovies.reset_index(drop=True)\n",
        "\n",
        "  # Supprimer les colonnes non nécessaires\n",
        "  userGenreTable= userMovies.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)\n",
        "\n",
        "  # Produit matriciel pour obtenir les poids\n",
        "  userProfile= userGenreTable.transpose().dot(inputMovies['rating'])\n",
        "\n",
        "  # Récupérons les genres de chaque film de notre dataframed'origine\n",
        "  genreTable= moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])\n",
        "\n",
        "  # Et supprimons less colonnes non nécessaires\n",
        "  genreTable= genreTable.drop('movieId', 1).drop('title', 1).drop('genres', 1).drop('year', 1)\n",
        "  genreTable.head()\n",
        "  genreTable.shape\n",
        "\n",
        "  # Multiplier les genres par les poids et calculer la moyenne pondérée\n",
        "  recommendationTable_df= ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())\n",
        "\n",
        "  # Ordonner les recommandations par ordre décroissant\n",
        "  recommendationTable_df= recommendationTable_df.sort_values(ascending=False)\n",
        "\n",
        "  # Le résultatfinal // On va chercher des films\n",
        "  recommanded_movies = movies_df.loc[movies_df['movieId'].isin(recommendationTable_df.head(20).keys())]\n",
        "  return recommanded_movies[:n_recommandations]"
      ],
      "metadata": {
        "id": "wDhJzo_J_k6-"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#Exemple d'utilisateur\n",
        "userInput= [\n",
        "        {'title':'Breakfast Club, The', 'rating':5},\n",
        "        {'title':'Toy Story', 'rating':2},\n",
        "        {'title':'Jumanji', 'rating':3.5},\n",
        "        {'title':'PulpFiction', 'rating':5},\n",
        "        {'title':'Akira', 'rating':4.5}"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "hBrtr4bSDifd",
        "outputId": "6fd4224f-8e20-4c9c-d483-a613609dafbe"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "5\n",
            "3.5\n",
            "2\n",
            "5\n",
            "4.5\n",
            "[{'title': None, 'rating': 5.0}, {'title': None, 'rating': 3.5}, {'title': None, 'rating': 2.0}, {'title': None, 'rating': 5.0}, {'title': None, 'rating': 4.5}]\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "class MoviesRecommandationsApp(Resource):\n",
        "  def __init__(self):\n",
        "    self.app_name = \"Home Movies theater\"\n",
        "    self.background_color = \"#5A595D\"\n",
        "    self.text_animation = \"fade-in-out\"\n",
        "\n",
        "  def post(self):\n",
        "    data = request.get_json()\n",
        "    userInput = userInput\n",
        "\n",
        "    #Utiliser la fonction de recommandation\n",
        "    recommanded_movies = Movies_Recommandations(userInput, ratings_df, moviesWithGenres_df)\n",
        "\n",
        "    return {\n",
        "        \"app_name\": self.app_name,\n",
        "        \"background_color\": self.background_color,\n",
        "        \"text_animation\": self.text_animation,\n",
        "        \"recommanded_movies\": recommanded_movies\n",
        "    }\n",
        "\n"
      ]
}
