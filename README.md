To run:

copy docker/local.env.example to docker/local.env
docker-compose up

Notes:
1. Example given in task description for provider_c in my opinion is incorrectly computed, math is 1st biggest topic, therefore value should be set to 10, not 12.5
2. For rare case of all three topics matching i chose best two as base value. Usually i would confirm such implementation with product owner, but obviously based on time i was working on this test, it wasn't possible


While writing this code i initially wanted to go with sql based storage for all providers (hence postgres inclusion in docker confs), however while working on test examples 
i spent too much time on figuring out provider_c value and i exceeded planned task time. If you prefer for me to rewrite it as i initially wanted (to use postgres relational tables for fast recommendation search please let me know)

Improvements for future:
1. SQL based storage for provider topics
2. Multi file spread, possibly using Blueprint for easier inclusion
3. Install script for SSL certs 
4. Put quote computation parameters into database, or at least use dictionaries isntead of if's
5. More edge case tests, obviously

   


