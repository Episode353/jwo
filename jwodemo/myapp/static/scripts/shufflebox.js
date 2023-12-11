$(function () {
    // Check if the shuffle parameter is present in the URL
    const urlParams = new URLSearchParams(window.location.search);
    const shufflePage = urlParams.get('shuffle');

    if (shufflePage) {
        const filePath = `../static/html-shuffle/${shufflePage}`;
        // Load the specified page indicated by the shuffle parameter
        $("#htmlshufflebox").load(filePath, function (response, status, xhr) {
            if (status === "error") {
                // Display an error message when the file does not exist
                const errorImages = '<img style="width:90%;" src="../media/gif/shuffle-error1.gif" alt="im sorry brough">' +
                    '<img style="width:90%;" src="../media/gif/shuffle-error-2.gif" alt="that link dont work doe">';
                $("#htmlshufflebox").html(errorImages);
            }
        });
    } else {
        var basePath = "../static/html-shuffle"; // Customize the base path here
        var files = [
            'gunt-fish.html', //
            'builder-dog.html',//
            'blender-fish.html',//
            'rat-night.html',//
            '4chan_idiot.html',//
            'wizard-ask.html',//
            'seep-rule.html',//
            'guiseppe.html',//
            'feesh-brain.html',//
            'fish-plan.html',//
            'stolen.html',//
            'david_death.html',
            'fly_edible.html',
            'dorito-time.html',
            'loud-ward.html',
            'twinks.html',
            'drake-trash.html',
            'arizona.html',
            'doyoumissher.html',
            'snoopy-rave.html',
            'garfield.html',
            'crying_on_floor.html',
            'sigma-grintset.html',
            'stole-inch.html',
            'man-eat-fish.html',
            'brough.html',
            'tornado_courage.html',
            'link_burn.html',
            'sky_error.html',
            'jig-dirsty.html',
            'wheatley_power.html',
            'mort_russia.html',
            'Ender4Mod_agust7_2013.html',
            'whats_jiggy_thinking_about.html',
            'missing_couch.html',
            'LETMEOUT.html',
            'me_when_mango.html',
            'blood_test.html',
            'sus_nug.html',
            'mordecai_smooth_head.html',
            'how_to_say_hi_in_mandarin.html',
            'chad-geenie.html',
            'gang_bob.html',
            'scan_forehead.html',
            'jig-711-banned.html',
            'seep-coin.html',
            'muppets_get_real.html',
            'pizza_tower_description.html',
            'funny_turtle.html',
            'marty_mcfly.html',
            'annoying_orange_mariokart.html',
            'sponge_gun.html',
            'joe_biden_flying.html',
            'wojack_overgrown.html',
            'sep_language.html',
            'fldsmdfr.html',
            'shitsnotgoingsowell.html',
            'spongebob_amongus_bottle.html',
            'your_formula_sir.html',
            'cole-slaw.html',
            'simple_dog.html',
            'kill_seppe.html',
            'ash_ketchup.html',
            'claw_hands.html',
            'heavy-mcqueen.html',
            'listenman.html',
            'eepys.html',
            'package_death.html',
            'dog_dance.html',
            'among_chicken.html',
            'apple-store-mong.html',
            'berryboy.html',
            'red-door.html',
            'ramen_crazy.html',
            'door_monster.html',
            'defeat.html',
            'springtrap.html',
            'chic_webcam.html',
            'squarebob.html',
            'talabanroblox.html',
            'wario-hung.html',
            'garfield-breast-reduction.html',
            'i-found-fish.html',
            'cyotee-divit.html',
            'avgndk.html',
            'Return_of_Soup.html',
            'evidence.html',
            'paddington.html',
            'doorway.html',
            'cat_money.html',
            'dollar_bob.html',
            'simpson_video.html',
            'squidman.html',
            'oreotako.html',
            'pimpbob.html',
            'patrickurinal.html',
            'fandeath.html',
            'ratatouierp.html',
            'goku-door.html',
            'clay-delivery.html',
            'poolsclosed.html',
            'no-gooning.html',
            'dontpickmeup-hissss.html',
            'mewhenwhenme.html',
            'mcrib.html',
            'idkifmonkeyisai.html',
            'livewetreaction.html',
            'murrchips.html',
            'bb_rot.html',
            'sadgoober.html',
            'whateverthisbigredthingiscalled.html',
            'rainbow-creature.html',
            'goo-goo-za-za.html',
            'mister-white.html',
            'its-just-a-room.html',
            'mortified_rugby.html',
            'bad-even-worse.html'
   
    
        ];
        // Use the current time in milliseconds as a seed for the random number generator
        var seed = new Date().getTime();
        var random = function () {
            var x = Math.sin(seed++) * 10000;
            return x - Math.floor(x);
        };

        var randomFile = files[Math.floor(random() * files.length)]; // Pick a random file
        $("#htmlshufflebox").load(`${basePath}/${randomFile}`); // Load the random file into the div
    }
});
