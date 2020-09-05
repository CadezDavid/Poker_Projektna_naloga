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

      body {
        font-family: Arial, Helvetica, sans-serif;
      }

      .row {
        margin: 0 -5px;
      }

      .row_poteze {
        margin: 0 -5px;
        height: 50px;
        width: 100%;
      }

      .row_karte {
        margin: 0 -5px;
        height: 250px;
      }

      .row_poteze:after {
        content: "";
        display: table;
        clear: both;
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

      .btn {
        border: none;
        background-color: inherit;
        padding: 14px 28px;
        font-size: 16px;
        cursor: pointer;
        display: inline-block;
      }

      .btn:hover {
        background: #eee;
      }

      .card {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        padding: 16px;
        text-align: center;
        background-color: #f1f1f1;
      }

      .slikica-1 {
        border-radius: 8px;
        box-shadow: 0 60px 120px 0 rgb(0, 0, 0);
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

      .circle_big_blind {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        text-align: center;
        padding-top: 7px;
        font-size: 7px;
        color: #fff;
        background: crimson;
        white-space: normal;
        cursor: pointer;
        pointer-events: none;
      }

      .circle_small_blind {
        width: 35px;
        height: 35px;
        border-radius: 50%;
        text-align: center;
        padding-top: 7px;
        font-size: 7px;
        color: #fff;
        background: rgb(0, 12, 179);
        white-space: normal;
        cursor: pointer;
        pointer-events: none;
      }

    </style>
  
  </head>


  <body>

    {{!base}}

  </body>

</html>