% rebase('base.tpl')

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

<form action="/" method="GET">
    <div style='text-align: right; padding-right: 20%; padding-top: 5%; font-size: 30px; color: burlywood;'>
    % if izid:
    <h2>ČESTITAMO, ZMAGALI STE!</h2>
    % else:
    <h2>To igro ste žal izgubili.</h2>
    % end
    <h3>Spodaj lahko začnete novo igro.</h3>
    <button type="submit" class='btn_home'>Začni novo igro</button>
    </div>
</form>

</body>