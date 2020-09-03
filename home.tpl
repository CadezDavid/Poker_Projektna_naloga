% rebase("base.tpl")

<h1>
    POKER
</h1>

<h2>
    Prosim, izberite si začetne nastavitve:
</h2>

<form action="/home/" method="post">
    <p>Število računalnikov:<input type="number" name="stevilo_racunalnikov" min="2" max="15">
    <p>Ime igralca:<input type="text" name="ime_igralca" placeholder="Vaše ime">
    <p>Začetni_denar:<input type="number" name="zacetni_denar" min="500" max="5000" step="100">
    <p><button type="submit">Pošlji</button>
</form>