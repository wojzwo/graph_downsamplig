# graph_downsamplig

Program do downsamplingu sygnałów, zasada działania opiera się o wykonywanie downsamplingu tylko na fragmentach sygnału bez interesujących zdarzeń.

Zaimplementowane jest kilka metod filtrowania sygnału których parametry można regulować:
-Filtrowanie zakłóceń sieciowych - częstotliwości ~50Hz i wyższych harmonicznych
-Filtr górnoprzepustowy z regulowanym odcięciem (domyślnie 4kHz)
-Matched filter - filtr opierajacy sie na cross-korelacji ze wzorem - domyslnie gauss o szerokości połówkowej 3.7 bina czasowego - 
dobrany dla zwiększenia Signal-Noise-Ratio dla impulsów znacznikowych diod. Sygnały zdarzeń są bardzo dobrze widoczne nad szumem a taki wzór ich nie osłabia.

Następnie przeprowadzamy rozpoznawanie zdarzeń z progiem th=-50.

Downsampling przeprowadzany jest na całym sygnale poza zdarzeniami i ich bezpośrednimi sąsiedztwem excess=200 najbliższych punktów.
Downsampling przeprowadzany jest z rate downsampling_rate=2000 - czyli wybierany jest co 2000 punkt.

Downsampling przeprowadzany jest zarówno na sygnale raw jak i przefiltrowanym mozna zobaczyc efekty na obu.

Uruchamianie z parametrem ścieżki do pliku do przerobienia:
downsampling.py "sciezka do pliku .mat"

