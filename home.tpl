% rebase("base.tpl")

<h1>
    <div class=>
    POKER
    </div>
</h1>

<h2>
    <div class='center'>
    Prosim, izberite si začetne nastavitve:
    </div>
</h2>

<form action="/home/" method="post" class="center">
    <p>Število računalnikov:<input type="number" name="stevilo_racunalnikov" min="2" max="15" autofocus>
    <p>Ime igralca:<input type="text" name="ime_igralca" autofocus>
    <p>Začetni_denar:<input type="number" name="zacetni_denar" min="500" max="5000" step="100" autofocus>
    <p><button type="submit">Pošlji</button>
</form>