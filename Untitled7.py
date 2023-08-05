{
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
