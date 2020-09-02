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

</head>

<body>
    <table width="100%">
        % for igralec in soba.igralci_v_sobi:
        <tr>
            
            % if soba.trenutna_igra.ime_osebe_na_potezi() == igralec:
                <th>Na potezi:</th>
            % else:
                <th>__________</th>
            % end
            
            % if igralec in soba.igralci_za_mizo:
            <th style="background-color:#00FF00">{{igralec}}</th>
            % else:
            <th style="background-color:#FF0000">{{igralec}}</th>
            % end
            
            % if igralec in soba.trenutna_igra.igralci_v_igri:
            <th>V igri</th>
            % else:
            <th>Ni igri</th>
            % end
            

            % if igralec in soba.igralci_za_mizo:
                % if soba.igralci_za_mizo.index(igralec) == soba.pozicija_big_blind:
                <th>Big_blind__</th>
                % elif soba.igralci_za_mizo.index(igralec) == soba.pozicija_small_blind:
                <th>Small_blind</th>
                % else:
                <th>___________</th>
                % end
            % else:
            <th>___________</th>
            % end

            % if igralec in soba.igralci_za_mizo:
                <th>{{soba.trenutna_igra.denar[igralec]}}</th>
                <th>{{soba.trenutna_igra.stava[igralec]}}</th>
                % if soba.trenutna_igra.konec:
                <th>{{soba.trenutna_igra.karte_igralcev[igralec]}}</th>
                % end
            % else:
            <th>___________</th>
            % end

            % if soba.trenutna_igra.konec and igralec == soba.trenutna_igra.zmagovalec:
            <th>Zmagovalec</th>
            % end
        
        </tr>
        % end
    </table>

    <table>
        <tr>
            % for karta in soba.trenutna_igra.karte_na_mizi:
            <th>
                <img src='/Slike/{{funkcije.alternativni_zapis(karta)}}.png' alt='Slika' width="120">
            </th>
            % end
        </tr>
    </table>

    <table>
        <tr>
            <img src='/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[soba.ime_igralca][0])}}.png' alt='Slika' width="120">
            <img src="/Slike/{{funkcije.alternativni_zapis(soba.trenutna_igra.karte_igralcev[soba.ime_igralca][1])}}.png" alt='Slika' width="120">
        </tr>
    </table>

    % if soba.ime_igralca == soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi] and not soba.trenutna_igra.konec:

        <form action='/igra/stava/{{id_sobe}}/' method='POST'>
            <input type='number' name='Stava' min='0' max='{{soba.trenutna_igra.denar[soba.trenutna_igra.igralci[soba.trenutna_igra.na_potezi]]}}' step='{{soba.small_blind}}'>
            <button type='submit'>Stavi</button>
        </form>
        
        <form action='/igra/fold/{{id_sobe}}/' method='POST'>
            <input type='submit' value='Fold'>
        </form>

        <form action='/igra/equal/{{id_sobe}}/' method='POST'>
            <input type='submit' value='Equal'>
        </form>

        % if soba.trenutna_igra.stava[soba.ime_igralca] == max([soba.trenutna_igra.stava[igralec] for igralec in soba.trenutna_igra.igralci]):
            <form action='/igra/check/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Check'>
            </form>
        % end

    % end

</body>

