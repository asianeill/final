# Detective Beaver

## Dillworth Duck is dead. There were five people in the building. This should be an easy case, right?

In this visual novel/game, you play a rookie detective. It's your first case. You and your partner, Detective Beaver, must explore the headquarters of megacorporation Coca-Koala. While interviewing the four suspects, you start to sense that something more is going on in Coca-Koala... perhaps, it's not just a drink company.

## Final project for CIS 1051

Please view script.rpy under the detectivebeaver folder to view code.

Link to video: https://youtu.be/II7OukGL6JA?si=lc9c_pc1XCvF_geg

Link to game: https://tun53946.itch.io/detective-beaver


## Details
There are a few clues you can choose to pick up along the way.

### There are 3 different endings, depending on when you complete the safe puzzle, and if you get the gun.

Ending 1: You knew the safe combination the first time and got the gun. Wasting no time, you, Blarf and Detective Beaver stop the Coca-Koala. At the end of the game, you get an end credit scene that shows Detective Beaver switching careers. He now sells Detective Beaver soda.

Ending 2: You didn't know the safe combination the first time, but you found the code and got the gun. Unfortunately, you were too late, and the Coca-Koala kills detective beaver in a creepy cut-scene. However, you shoot the Coca-Koala in the hand and save the city. At the end of the game, you wonder what happened to Blarf. You are shown an end-credit scene of Blarf in a room full of cocaine.

Ending 3: You could not get into the safe and did not get the gun. Detective Beaver is shot by the Coca-Koala, in a creepy cut-scene. Instead of stopping the Coca-Koala, you ask to join him. It is revealed that you, the main character, are a koala. You and the Coca-Koala run the city and make millions. At the end of the game, you wonder what happened to Blarf. You are shown an end-credit scene where Blarf becomes a cop and busts you.

## Attributions:
All characters drawn/photoshopped by Asia

All items either made in Adobe Photoshop by Asia, or found on Adobe Stock

All videos where made by Asia, using Adobe Premiere Pro

Backgrounds from Adobe Stock

### Music:
Game background music: https://www.youtube.com/watch?v=qgPSTtl3zOU&t=50s

Security cam overlay: https://www.youtube.com/watch?v=Cqxd43BS5VQ&t=7s

Dust overlay for security cam: https://www.youtube.com/watch?v=oh1FxN0nMkQ&t=5s

Detective Beaver advertisement end credit song: https://www.youtube.com/watch?v=FPRUTp3Hp7k

Blarf police end credit song: https://www.youtube.com/watch?v=FXzH8EMagt4&t=29s

Police siren overlay: https://www.youtube.com/watch?v=-C6oSIvd5NM

Blarf is addicted to cocaine end credit song: https://www.youtube.com/watch?v=XuK-MKGb3E8

Detective Beaver dies horror music: https://www.youtube.com/watch?v=EG71G97Q7Zo\

Gunshot sound effect: https://www.youtube.com/watch?v=q6Vj40bdbho

### Tutorials used:
Paper puzzle made using tutorial: https://www.youtube.com/watch?v=IKLBSJMv50Q&t=1s


Safe puzzle made using tutorial: https://www.youtube.com/watch?v=_0mvFUwyMwY&t=3s

I learned how to use renpy from Lemma Soft Forums and renpy.org.

## Notes
Challenges faced: My biggest challenge came after I spent 5 hrs following tutorials on how to make the puzzles in renpy. For the safe puzzle, I ran into a bug where the safe wouldn't always disappear. I fixed it by including the following:

Here, I hid the layers and jumped to a new scene.

if current_safe == 1:

        imagebutton auto "gun-%s.png" focus_mask True action [Hide(screen=None, transition=dissolve, _layer=None), Jump("getgun"),] at half_size

Here, I made it so if you click on the red handle, it hides the layers and jumps to a new scene.

if combination_check == "wrong":

        imagebutton auto "images/safe-handle-ind-red-%s.png" focus_mask True action [Hide(screen=None, transition=dissolve, _layer=None), Play(file = "audio/locked-door.ogg", channel = "sound"), Jump("nogun"),] at half_size

Here, if the reset button is clicked, the layers are hidden and it jumps back a scene. The tutorial's reset button didn't work how I wanted it to.

        imagebutton auto "images/dial-reset-button-%s.png" align(0.5, 0.5) focus_mask True action [Hide(screen=None, transition=dissolve, _layer=None), Jump("reset")] at half_size 

I also ran into an issue where the puzzle pieces were locking into incorrect places. However, I fixed this by playing around with the coordinates in the list.

Overall,

I had so much fun making this! One night, I stayed up all night working on it because I didn't want to stop. Genuinely, the most fun I've had on a college assignment. Thanks for giving us an open-ended final project! 




