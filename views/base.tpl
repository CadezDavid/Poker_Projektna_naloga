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

      .btn_home {
        border: none;
        color: burlywood;
        background-color: inherit;
        padding: 14px 28px;
        font-size: 30px;
        cursor: pointer;
        display: inline-block;
      }

      .btn_naslednja {
        border: none;
        background: burlywood;
        padding: 14px 28px;
        font-size: 20px;
        cursor: pointer;
        display: inline-block;
      }

      .btn:hover {
        background: #eee;
      }

      .btn_home:hover {
        background: burlywood;
        color:rgb(0, 0, 0)
      }

      .btn_naslednja:hover {
        border: none;
        background: burlywood;
        padding: 14px 28px;
        font-size: 20px;
        cursor: pointer;
        display: inline-block;
      }

      .card {
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        padding: 16px;
        text-align: center;
        background-color: #f1f1f1;
      }

      .slikica-1-0 {
        border-radius: 8px;
        box-shadow: 0 60px 120px 0 black;
      }

      .slikica-0-0 {
        border-radius: 8px;
      }

      .slikica-1-1 {
        border-radius: 8px;
        box-shadow: 0 100px 120px 0 green;
      }

      .slikica-0-1 {
        border-radius: 8px;
        box-shadow: 0 120px 150px 0 green;
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

      .pomoc {
        position: relative;
        display: inline-block;
      }

      .pomoc .besedilo {
        visibility: hidden;
        background-color: black;
        color: #fff;
        bottom: 125%;
        right: 150%;
        left: -800%;
        text-align: center;
        padding-bottom: 5px;
        padding-top: 5px;
        padding-left: 5px;
        padding-right: 5px;
        border-radius: 6px;
        position: absolute;
      }

      .pomoc:hover .besedilo {
        visibility: visible;
      }

    </style>
  
  </head>


  <body>

    {{!base}}

  </body>

</html>