mpmetis graphs/metis.mesh 10
gpmetis graphs/mdual.graph 10
ndmetis graphs/mdual.graph 10
gpmetis graphs/test.mgraph 10
m2gmetis graphs/metis.mesh 10


set -ex



graphchk
cmpfillin -h
mpmetis -h
gpmetis -h
ndmetis -h
gpmetis -h
m2gmetis -h
test -f $PREFIX/include/metis.h
test -f $PREFIX/lib/libmetis.so
exit 0
