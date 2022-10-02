import random
Randomint=int(f'{random.randrange(1, 10**3):03}')
a1 = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title>
   <link rel= "stylesheet" type= "text/css" href= "{{{{url_for('static',filename='style.css') }}}}">
</head>
  <body>
  <h1>Stock/Crypto portfolio</h1>
  <p>if you want to help the project please consider donating, BCH and matic friendly!</p>
  <h1>Here are your results</h1>
  <div class="Cen">
    {table}
  <img src="{{{{url_for('static', filename='polygon-matic.gif')}}}}" />
 <div class="GraphCont">
  <h2 class="TItulo">Graph</h2>'''
a2='''
  <img src="{{{{url_for('static', filename='Portfolio project\static'''
  

a3=f'''\{Randomint}')'''
a4='''}}}}" />
  </div>
  </div>
  <footer>
    <a class="Links" href="{{{{url_for('donate')}}}}">Donate!</a>
    <a class="Links" href="https://twitter.com/LilElseCaller">Twitter</a>
    <a class="Links" href="https://medium.com/@LilElseCaller">Medium</a>
    <a class="Links" href="https://github.com/egarcia00">Algo Creator</a></p>
    

</footer>
  </body>
</html>
'''

html_string=a1+a2+a3+a4
print(html_string)