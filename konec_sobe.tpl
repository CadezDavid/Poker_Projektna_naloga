% rebase('base.tpl')
% import poker

% if not izid:


<div style='text-align: center;'>
<h3>To igro ste žal izgubili.</h3>
</div>


<div style='text-align: center;'>
    <h3>
        Imate naslednje možnosti:
        <form action="/" method="get" class="center">
            <input type="submit" name="Nova igra." autofocus>
        </form>
    </h3>
</div>


% elif izid:

<div style='text-align: center;'>
    <h3>Čestitam, zmagali ste.</h3>
</div>
    
    
<div style='text-align: center;'>
    <h3>
        Imate naslednje možnosti:
        <form action="/" method="get" class="center">
            <input type="submit" name="Nova igra." autofocus>
        </form>
    </h3>
</div>

% end