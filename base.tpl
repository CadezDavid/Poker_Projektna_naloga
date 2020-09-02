<!doctype html>

<html lang='en'>

  <head>
    <title>Poker</title>
    <meta charset='utf8'>
    <meta name="viewport" content="width=device-width, initial-scale=1">
  
    <style>
      * {
        box-sizing: border-box;
      }

      .igralceva_mizica {
        background-color: slategrey;
        padding: 15px;
      }

      body {
        font-family: Arial, Helvetica, sans-serif;
      }

      .row {
        margin: 0 -5px;
      }

      .row:after {
        content: "";
        display: table;
        clear: both;
      }

      @media screen and (max-width: 600px) {
        .column {
          width: 100%;
          display: block;
          margin-bottom: 20px;
        }
      }

      .card {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        padding: 16px;
        text-align: center;
        background-color: #f1f1f1;
      }

      .token_big_blind {
        background-color: gold;
        text-align: center;
        text-decoration-color:black;
        display: block;
        height: 90px;
        width: 90px;
        border-radius: 50%;
        border: none;
        text-align: center;
        font-size: 17px;
        white-space: normal;
        cursor: pointer;
        pointer-events: none;
      }
      
      .token_small_blind {
        background-color:mediumblue;
        text-align: center;
        display: block;
        color: white;
        height: 90px;
        width: 90px;
        border-radius: 50%;
        border: none;
        text-align: center;
        font-size: 17px;
        white-space: normal;
        cursor: pointer;
        pointer-events: none;
      }

      .slikica-1 {
        border-radius: 8px;
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 2);
      }

      .slikica-0 {
        border-radius: 8px;
      }

      .container {
        position: relative;
        width: 50%;
      }

      .overlay {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        height: 100%;
        width: 100%;
        opacity: 40%;
        background-color: slategrey;
      }

    </style>
  
  </head>


  <body>

    {{!base}}

  </body>

</html>