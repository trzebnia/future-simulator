# future-simulator
### Idea
The idea for this project started the first time I have seen the "timelapse of the future" video on youtube by melodysheep: https://www.youtube.com/watch?v=uD4izuDMUQA
The video presents the future of the universe where starting from 1 year per second the speed of simulation doubles every 5 seconds.
Considering that protons do decay, time (relatively) quickly becomes meaningless as universe reaches maximum entropy after last black holes evaporate,
around 10^100 years into the future.
This point is reached after about 27 minutes of simulation.
But I am not a fan of the proton dacay theory so I wanted to see how a simulation without it would look like.
But I quickly realized that in such simulation it would be impossible to reach later events in human lifetime.

### Purpose
That's why I decided to just accelerate the simulation even more by giving it more "accelerators".
The main idea of this project is operating on numbers than maximum value of float (which is a bit over 10^308).
Reaching this point with only the accelerator from the video would take 85 minutes, while by just adding 1 more accelerator (doubling the value of first every 5 seconds)
It can be reached in less than 4 minutes.
The whole idea of feeling the time passing changes a bit as instead of just seeing it grow exponentially, we see the exponents grow exponentially.

### Issues
There are a few penalties for trying to reach big numbers.
The numbers start loosing precision after reaching 10^200.
The addition won't work if difference beetwen exponents is higher than 100. It starts happening sooner the more accelerators and more powerful there are,
but usually around the time it starts happening the addition becomes meaningles.
The multiplication should work for a lot longer, easily up to 10^10^300, but again after this point it would only work with small enough differences.
Another problem is that after reaching about 10^10^8 the program slows down significantly.
I lose patience after 10^10^10 but in theory it should be able to get to 10^10^120 (although it seems to keep slowing down so it could take extremely long).

### Important
I upload both the code and complite file of the latest version, but if anyone wants to actually run the program I would recommend running the script with python interpreter,
as the exe isn't liked by quite a few antiviruses.
The one I am using started accepting it and all new versions after a few days of deleting it so it's possible that someday it will be accepted by the rest.

### Future plans
If I ever get back to this project I will try to workout what exactly antiviruses don't like in it and fix the performance issue 
(I know it is probably written terribly but to be honest after so many fails I just wanted it to work)
