% rebase("base.tpl")

<head>
    <style>
        html { 
          background: url(/Slike/ozadje.jpg) no-repeat center center fixed; 
          -webkit-background-size: cover;
          -moz-background-size: cover;
          -o-background-size: cover;
          background-size: cover;
        }
    </style>
</head>

<body>


<form action="/home/" method="post">
    <div style='text-align: right; padding-right: 20%; padding-top: 5%; font-size: 30px; color: burlywood;'>
    <h2>POKER</h2>
    <h3>Prosim, izberite si začetne nastavitve:</h3>
    <p>Število računalnikov: <input type="number" name="stevilo_racunalnikov" value="5" min="2" max="15">
    <p>Ime igralca: <input type="text" name="ime_igralca" placeholder="Vaše ime" required>
    <p>Začetni denar: <input type="number" name="zacetni_denar" value="2000" min="500" max="5000" step="100">
    <p><button type="submit" class='btn_home'>Pošlji</button>
    </div>
</form>

</body>