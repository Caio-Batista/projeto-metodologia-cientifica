all:
	./classificar_test "-v" "emails/treino/" "emails/teste"

clean:
	rm *.csv *.arff
