% rebase('base.tpl')
% import poker

% if not izid:

To igro ste izgubili. Še sreča, da ne igrate s pravim denarjem.

Imate naslednje možnosti:
<form action="/" method="get" class="center">
    <input type="submit" name="Nova igra." autofocus>
</form>

% elif izid:

Čestitam, zmagali ste.

Imate naslednje možnosti:
<form action="/" method="get" class="center">
    <input type="submit" value="Nova igra.">
</form>