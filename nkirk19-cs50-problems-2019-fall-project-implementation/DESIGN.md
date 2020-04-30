We used several Python libraries in the creation of CCP1.py. They are requests,
pandas, seaborn, matplotlib, plotly, and numpy. We used requests to access the
the datasets that were available online.

Requests allowed us to directly access the files via the Internet rather than having to store them locally.

We used pandas to manipulate the data. In many ways, pandas is similar to using SQL
except it is directly in Python, which made coding a little easier and more organized.
Pandas allowed for us to parse the information from the publicly available datasets
(which had much more information than we actually needed), store the desired information
in a new Excel file, and then, at the end, merge all of our individual datasets into one
big dataset which centralized all of the information along the FIPS codes (which are like a
primary key in SQL).

Seaborn, matplotlib, and plotly allowed us to create maps, graphs, and other
visualizations to make the data easier to understand. For example, matplotlib and plotly allowed
us to make the choropleth maps to show the range of data across the U.S. Seaborn allowed us to
correlate every variable against each other in a very simple manner, outputting a heatmap and all
of the correlation charts.

In CCP1.py, we created functions like CreateChoropleth and process because it made it so we wouldn't
have to repeat the same code. After all, each data set was going to go through the same exact process,
so making a function made this a streamlined process. We also specified where to save files at the top
because we knew we would be saving lots of files, so this made it so we didn't have to hard code
directories every single time. Our logic is pretty linear: take each dataset, parse it, join it with FIPS codes,
make a choropleth map, and, once all of them are done, join all the datasets together into one centralized structure
and make correlations and a heatmap for that big dataset. There were a couple times, like with seaborn, for example,
where we had to play around with the code to change how the graph outputted. We wanted to make the graphs as pretty
as possible so that they made the data easy to visualize.

The sole reason we used CCP1.py on a local machine is because the IDE couldn't handle the script without
killing it. This made directly putting the plotly graphs into our Flask script quite difficult (we found
resources online that would have helped us to directly embed the plotly output into the html files
displayed on our Flask-based website). Unforunately, we were forced to then move everything over to the IDE manually –
not that we wanted to! We used Flask because it would allow us to make our page a bit more dynamic than a simple HTML structure
like in Homepage. Application.py is very much like Finance, so we styled it that way because we were familiar with
that style. We also used Bootstrap to bolster our CSS because it made it easy (and pretty)!