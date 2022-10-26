rm master.log
nohup locust -f load_test_warm.py --master > master.log &

rm worker*.log
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker1.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker2.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker3.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker4.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker5.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker6.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker7.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker8.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker9.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker10.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker11.log &
nohup locust -f load_test_warm.py --worker --master-host=localhost > worker12.log &


