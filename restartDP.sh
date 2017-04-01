echo "Geplanter Neustart DP-Fernzugang..."

sudo supervisorctl stop tuxtunnel
nohup sudo supervisorctl restart tuxtunnel >/dev/null 2>&1 &

echo "Fertig."