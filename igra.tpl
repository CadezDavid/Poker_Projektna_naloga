% rebase ('base.tpl')
% import poker
% import funkcije

<html>

<head>
<title>Poker</title>
<meta charset='utf8'>
% if ime_sobe.ime_igralca != igra.igralci[igra.na_potezi]:
<meta http-equiv="refresh" content="2;URL=http://127.0.0.1:8080/igra/racunalnikovi_manevri/{{id_sobe}}/">
% end
</head>

<body>
    <table width="100%">
        % for igralec in igra.igralci:
        <tr>
            % if igra.igralci[igra.na_potezi % len(igra.igralci)] == igralec:
                <th>Na potezi:</th>
            % else:
                <th>__________</th>
            % end
            <th>{{igralec}}</th>
            % if igra.igralci_v_igri[igralec]:
            <th>V igri</th>
            % else:
            <th>Ni igri</th>
            % end
            <th>{{igra.denar[igralec]}}</th>
            <th>{{igra.stava[igralec]}}</th>
        </tr>
        % end
    </table>

    <table>
        <tr>
            % for karta in igra.karte_na_mizi:
            <th>
                {{karta}}
            </th>
            % end
        </tr>
    </table>

    <table>
        <tr>
            {{igra.karte_igralcev[ime_sobe.ime_igralca]}}
        </tr>
    </table>

    % if ime_sobe.ime_igralca == igra.igralci[igra.na_potezi]:

        <form action='/igra/stava/{{id_sobe}}/' method='POST'>
            <input type='number' name='Stava' autofocus>
            <button type='submit'>Stavi</button>
        </form>
        
        <form action='/igra/fold/{{id_sobe}}/' method='POST'>
            <input type='submit' value='Fold'>
        </form>

        % if igra.stava[ime_sobe.ime_igralca] == max([igra.stava[igralec] for igralec in igra.igralci]):
            <form action='/igra/check/{{id_sobe}}/' method='POST'>
                <input type='submit' value='Check'>
            </form>
        % end

    % end

</body>

</html>