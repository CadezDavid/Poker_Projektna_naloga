% rebase ('base.tpl')
% import poker
% import funkcije
% import Slike


<head>

% if soba.ime_igralca != soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi] and not soba.trenutna_igra.konec:
<meta http-equiv="refresh" content="0.2;URL=http://127.0.0.1:8080/igra/racunalnikovi_manevri/{{id_sobe}}/">
% end

<style>
    .column {
        float: left;
        align-content: center;
        text-align: center;
        width: {{100 / (len(soba.igralci_za_mizo) - 1)}}%;
        padding: 0 10px;
    }

    .column_spodej {
        float: left;
        align-content: center;
        text-align: center;
        width: 33%;
        padding: 0 10px;
    }

    .gumbki {
        float: left;
        align-content: center;
        text-align: center;
        width: 33%;
        padding: 0 10px;
    }

    .igralceva_mizica-0 {
        background-color: slategrey;
        padding: 15px;
    }

    .igralceva_mizica-1 {
        background-color: darkslategray;
        padding: 15px;
    }
  
</style>

</head>

<body>

    <div class='row'>
        
        % for igralec in soba.igralci_za_mizo:
            
        % if igralec != soba.ime_igralca:
        
            <div class="column">
            <img src="/Slike/{{soba.slike_igralcev[igralec]}}.jpg" width='100' class="slikica-{{int(igralec == soba.trenutna_igra.ime_osebe_na_potezi() and not soba.trenutna_igra.konec)}}-{{int(soba.trenutna_igra.konec and igralec in soba.trenutna_igra.zmagovalec)}}" alt='Slika igralca' height='100'>
                <div class="card-body">
                    <h5 class="card-title">{{igralec}}</h5>
                    <p class="card-text">
                        <p>Denar: {{soba.trenutna_igra.denar[igralec]}}</p>
                        <p>Stava: {{soba.trenutna_igra.stava[igralec]}}</p>
                        
                        % if igralec == soba.trenutna_igra.igralec_z_big_blind():
                        <img src='/Slike/big_blind.png' width='50px'>
                        % end

                        % if igralec == soba.trenutna_igra.igralec_s_small_blind():
                        <img src='/Slike/small_blind.png' width='50px'>
                        % end

                        % if igralec in soba.trenutna_igra.igralci_v_igri:
                        <img src='/Slike/pair-of-cards.png' width='50px'>
                        % end

                        <p>
                            % if soba.trenutna_igra.konec:
                            <img src='/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[igralec][0])}}.png' alt='Slika' width="50">
                            <img src="/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[igralec][1])}}.png" alt='Slika' width="50">
                            % end
                        </p>
                </div>
            </div>
        
        % end
    
        % end
    
    </div>

    % if soba.trenutna_igra.konec:

    % if len(soba.trenutna_igra.igralci_v_igri) == 1:
    <form action='/zacetek_igre/{{id_sobe}}/' method='GET'>
    <p><h2 style='text-align: center;'>
    Zmagal je {{soba.trenutna_igra.zmagovalec[0]}}, ker so ostali odstopili.
    <button type='submit' value='Naslednja igra' class='btn_naslednja'>Naslednja igra</button>
    </p></h2>
    </form>
    % elif len(soba.trenutna_igra.zmagovalec) == 1:
    <form action='/zacetek_igre/{{id_sobe}}/' method='GET'>
    <p><h2 style='text-align: center;'>Zmagal je {{soba.trenutna_igra.zmagovalec[0]}}. V rokah je imel {{funkcije.slovar_zmagovalnih_kart[soba.trenutna_igra.zmagovalne_karte[0][0]]}}.
    <button type='submit' value='Naslednja igra' class='btn_naslednja'>Naslednja igra</button>
    </p></h2>
    </form>
    % else:
    <h2>
    
    <form action='/zacetek_igre/{{id_sobe}}/' method='GET'>
        Zmagali so:
        % for i in range(len(soba.trenutna_igra.zmagovalec) - 1):
        {{soba.trenutna_igra.zmagovalec[i]}} ({{funkcije.slovar_zmagovalnih_kart[soba.trenutna_igra.zmagovalne_karte[i][0]]}}),
        % end
        {{soba.trenutna_igra.zmagovalec[-1]}} ({{funkcije.slovar_zmagovalnih_kart[soba.trenutna_igra.zmagovalne_karte[-1][0]]}}).
        <button type='submit' class='btn_naslednja'>Naslednja igra</button>
    </form>

    </h2>

    % end


    <table width=30% style='clear: both;'>
        <tr>
            % for karta in soba.trenutna_igra.karte_na_mizi:
            <th>
                <img src='/Slike/{{funkcije.alternativni_zapis(karta)}}.png' alt='Slika' width="120">
            </th>
            % end
        </tr>
    </table>

    % else:

    <table width=30% style='clear: both;'>
        <tr>
            % for karta in soba.trenutna_igra.karte_na_mizi:
            <th>
                <img src='/Slike/{{funkcije.alternativni_zapis(karta)}}.png' alt='Slika' width="120">
            </th>
            % end
        </tr>
    </table>

    % end
    
    <div class='igralceva_mizica-{{int(soba.trenutna_igra.ime_osebe_na_potezi() == soba.ime_igralca)}}'>
    <div class='row'>

        <div class='column_spodej'>

            <img src='/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[soba.ime_igralca][0])}}.png' alt='Slika' width="120">
            <img src="/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[soba.ime_igralca][1])}}.png" alt='Slika' width="120">
            % if soba.ime_igralca == soba.trenutna_igra.igralec_z_big_blind():
            <img src='/Slike/big_blind.png' width='70px' style='padding-left: 20px; padding-bottom: 150px;'>
            % elif soba.ime_igralca == soba.trenutna_igra.igralec_s_small_blind():
            <img src='/Slike/small_blind.png' width='70px' style='padding-left: 20px; padding-bottom: 150px;'>
            % end

        </div>
        

        % if soba.trenutna_igra.ime_osebe_na_potezi() == soba.ime_igralca:
        
        <div class='gumbki'>
            
            <form action='/igra/stava/{{id_sobe}}/' method='POST'>
                <input type='number' name='Stava' min='{{soba.trenutna_igra.min_stava() - soba.trenutna_igra.stava[soba.ime_igralca] + soba.small_blind()}}' max='{{soba.trenutna_igra.denar[soba. trenutna_igra.igralci[soba.trenutna_igra.na_potezi]]}}' step='{{soba.small_blind()}}' required>
                <input type='submit' value='Stavi' class='btn'>
            </form>

            <form action='/igra/odstop/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Odstop' class='btn'>
            </form>

            <form action='/igra/izenaci/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Izenači' class='btn'>
            </form>

            % if soba.trenutna_igra.stava[soba.ime_igralca] == max([soba.trenutna_igra.stava[igralec] for igralec in soba.trenutna_igra.igralci]):
                <form action='/igra/naprej/{{id_sobe}}/' method='POST'>
                    <input type='submit' value='Naprej' class='btn'>
                </form>
            % end

            <img src='/Slike/big_blind.png' width='30px' style='padding-top: 10px;'> - {{soba.big_blind}}
            <img src='/Slike/small_blind.png' width='30px' style='padding-top: 10px;'> - {{soba.small_blind()}}

        </div>

        % else:

        <div class='gumbki'>


            
            <form action='/igra/stava/{{id_sobe}}/' method='POST'>
                <input type='number' name='Stava' min='0' max='{{soba.trenutna_igra.denar[soba. trenutna_igra.igralci[soba.trenutna_igra.na_potezi]]}}' step='{{soba.small_blind()}}' disabled>
                <input type='submit' value='Stavi' class='btn' disabled>
            </form>

            <form action='/igra/odstop/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Odstop' class='btn' disabled>
            </form>

            <form action='/igra/izenaci/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Izenači' class='btn' disabled>
            </form>

            <img src='/Slike/big_blind.png' width='30px' style='padding-top: 10px;'> - {{soba.big_blind}}
            <img src='/Slike/small_blind.png' width='30px' style='padding-top: 10px;'> - {{soba.small_blind()}}
        
        </div>

        % end



        <div class='column_spodej'>
        <h4>{{soba.ime_igralca}}</h4>
        <p>Denar: {{soba.trenutna_igra.denar[soba.ime_igralca]}}</p>
        <p>Stava: {{soba.trenutna_igra.stava[soba.ime_igralca]}}</p>
        <div class="pomoc">Pomoč
            <span class="besedilo">
                Pojasnila vmesnika:
                <p>Vaša armatura se obarva temneje, ko ste na vrsti.
                <p>Na začetku je pred vsakim igralcem slika dveh majhnih kart. Ko ta slika izgine, je igralec odstopil od trenutne igre.
                <p>Vsaka stava v igri mora biti večkratnik small blinda.
                <p>Staviti morate vsaj toliko, kolikor je vsota največje stave na mizi in small blinda.
            </span>
        </div>
        <div style='padding-top: 30px'>
            <form action='/'>
                <input type='submit' value='Nova soba' class='btn'>
            </form>
        </div>

        </div>

    </div>
    </div>

</div>
</div>
</body>