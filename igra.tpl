% rebase ('base.tpl')
% import poker
% import funkcije
% import Slike


<head>

% if soba.ime_igralca != soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi % len(soba.trenutna_igra.igralci)] and not soba.trenutna_igra.konec:
<meta http-equiv="refresh" content="0.5;URL=http://127.0.0.1:8080/igra/racunalnikovi_manevri/{{id_sobe}}/">
% end
% if soba.trenutna_igra.konec:
<meta http-equiv="refresh" content="5;URL=http://127.0.0.1:8080/zacetek_igre/{{id_sobe}}/">
% end
<link rel="stylesheet" type="text/css" href="bootstrap.css">

<style>
    .column {
        float: left;
        width: {{100 / len(soba.igralci_za_mizo)}}%;
        padding: 0 10px;
      }
    
    .column_spodej {
        float: left;
        width: 33%;
        padding: 0 10px;
      }
</style>

</head>

<body>
    <div class='row'>
% for igralec in soba.igralci_za_mizo:
    
% if igralec == soba.ime_igralca:

% else:
    <div class="column">
    <!-- <img src="/Slike/{{soba.slike_igralcev[igralec]}}.jpg" width='100' class="card-img-top" alt='Slika igralca'> -->
        <div class="card-body">
            <h5 class="card-title">{{igralec}}</h5>
            <p class="card-text">
                <p>Denar: {{soba.trenutna_igra.denar[igralec]}}</p>
                <p>Stava: {{soba.trenutna_igra.stava[igralec]}}</p>
                % if igralec == soba.trenutna_igra.ime_osebe_na_potezi():
                <p>NA POTEZI</p>
                % else:
                <p>_________</p>
                % end
                % if igralec == soba.trenutna_igra.igralci[soba.pozicija_big_blind]:
                <p>BIG_BLIND__</p>
                % elif igralec == soba.trenutna_igra.igralci[soba.pozicija_small_blind]:
                <p>SMALL_BLIND</p>
                % else:
                <p>___________</p>
                % end
            </p>
        </div>
    </div>

% end
% end
    </div>
    
    
    <table>
        <tr>
            % for karta in soba.trenutna_igra.karte_na_mizi:
            <th>
                <img src='/Slike/{{funkcije.alternativni_zapis(karta)}}.png' alt='Slika' width="120">
            </th>
            % end
        </tr>
    </table>


    <div class='row'>

        <div class='column_spodej'>

            <img src='/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[soba.ime_igralca][0])}}.png' alt='Slika' width="120">
            <img src="/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[soba.ime_igralca][1])}}.png" alt='Slika' width="120">

        </div>
        
        <div class='column_spodej'>

            <form action='/igra/stava/{{id_sobe}}/' method='POST'>
                <input type='number' name='Stava' min='0' max='{{soba.trenutna_igra.denar[soba. trenutna_igra.igralci[soba.trenutna_igra.na_potezi]]}}' step='{{soba.small_blind}}   '>
                <button type='submit'>Stavi</button>
            </form>

            <form action='/igra/fold/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Fold'>
            </form>

            <form action='/igra/equal/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Equal'>
            </form>

            % if soba.trenutna_igra.stava[soba.ime_igralca] == max([soba.trenutna_igra.stava    [igralec] for igralec in soba.trenutna_igra.igralci]):
                <form action='/igra/check/{{id_sobe}}/' method='POST'>
                    <input type='submit' value='Check'>
                </form>
            % end

        </div>

        <div class='column_spodej'>
        
        <p>Denar: {{soba.trenutna_igra.denar[soba.ime_igralca]}}</p>
        <p>Stava: {{soba.trenutna_igra.stava[soba.ime_igralca]}}</p>

        </div>

    </div>

</div>
</body>