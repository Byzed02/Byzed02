{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOX1FDHCUp3pIOIL9HjetAe",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Byzed02/Byzed02/blob/main/Untitled7.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "mzKjO1ceCo5F"
      },
      "outputs": [],
      "source": [
        "total_points = st.slider(\"Number of points in spiral\", 1, 5000, 2000)\n",
        "num_turns = st.slider(\"Number of turns in spiral\", 1, 100, 9)\n",
        "\n",
        "Point = namedtuple('Point', 'x y')\n",
        "data = []\n",
        "\n",
        "points_per_turn = total_points / num_turns\n",
        "\n",
        "for curr_point_num in range(total_points):\n",
        "    curr_turn, i = divmod(curr_point_num, points_per_turn)\n",
        "    angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn\n",
        "    radius = curr_point_num / total_points\n",
        "    x = radius * math.cos(angle)\n",
        "    y = radius * math.sin(angle)\n",
        "    data.append(Point(x, y))\n",
        "\n",
        "st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)\n",
        "    .mark_circle(color='#0068c9', opacity=0.5)\n",
        "    .encode(x='x:Q', y='y:Q'))"
      ]
    }
  ]
}