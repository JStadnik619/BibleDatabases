import re
from collections import defaultdict

# TODO: Omit last blank line in chapter
def verses_followed_by_blank_line(text: str) -> dict[str, dict[int, list[int]]]:
    result = defaultdict(lambda: defaultdict(list))

    current_book = None
    current_chapter = None
    current_verse = None

    verse_pattern = re.compile(r'^\S+(?:\s+\S+)?\s+(\d+):(\d+)\t')
    divider_pattern = re.compile(r'^[-_]{10,}$')

    lines = text.splitlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect book heading
        if divider_pattern.match(stripped):
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if (
                j < len(lines)
                and lines[j].strip()
                and j + 1 < len(lines)
                and divider_pattern.match(lines[j + 1].strip())
            ):
                current_book = lines[j].strip().title()
                continue

        # Blank line => previous verse ended a paragraph
        if not stripped:
            if (
                current_book is not None
                and current_chapter is not None
                and current_verse is not None
            ):
                verses = result[current_book][current_chapter]
                if not verses or verses[-1] != current_verse:
                    verses.append(current_verse)
            continue

        # Verse line
        match = verse_pattern.match(line)
        if match:
            current_chapter = int(match.group(1))
            current_verse = int(match.group(2))

    return {
        book: {
            chapter: verses
            for chapter, verses in chapters.items()
        }
        for book, chapters in result.items()
    }

text ="""
----------------------------------------------------------------------------------------------
2 PETER
----------------------------------------------------------------------------------------------
2 Pe	The Second Letter of
 Peter

CHAPTER 1
2 Pe 1:1	Simeon Peter, a slave and apostle of Jesus Christ, to those who have obtained a faith equal in value to ours by the righteousness of our God and Savior Jesus Christ.
2 Pe 1:2	May grace and peace be multiplied to you in the knowledge of God and of Jesus our Lord,
2 Pe 1:3	because his divine power has bestowed on us all [things] [that are] necessary for life and godliness, through the knowledge of the one who called us by his own glory and excellence of character,
2 Pe 1:4	through which things he has bestowed on us his precious and very great promises, so that through these you may become sharers of the divine nature [after]<note: *Here "[after]" is supplied as a component of the participle ("escaping from") which is understood as temporal> escaping from the corruption [that is] in the world because of evil desire,
2 Pe 1:5	and [for] this same [reason], and [by]<note: *Here "[by]" is supplied as a component of the participle ("applying") which is understood as means> applying all diligence, supply with your faith excellence of character, and with excellence of character, knowledge,
2 Pe 1:6	and with knowledge, self-control, and with self-control, patient endurance, and with patient endurance, godliness,
2 Pe 1:7	and with godliness, brotherly love, and with brotherly love, love. 

2 Pe 1:8	For [if]<note: *Here "[if]" is supplied as a component of the participle ("are") which is understood as conditional> these [things] are yours and are increasing, this does not make [you] useless or unproductive in the knowledge of our Lord Jesus Christ.
2 Pe 1:9	For [the one] for whom these [things] [are] not present is blind, being nearsighted, {having forgotten the cleansing}<note: Literally "receiving forgetfulness of the cleansing"> of his former sins.
2 Pe 1:10	Therefore, brothers, be zealous even more to make your calling and election secure, because [if you]<note: *Here "[if]" is supplied as a component of the participle ("do") which is understood as conditional> do these [things], you will never ever stumble.
2 Pe 1:11	For in this way entrance into the eternal kingdom of our Lord and Savior Jesus Christ will be richly supplied for you. 

2 Pe 1:12	Therefore I intend to remind you continually concerning these [things], although [you] know [them] and are established in the truth that you have.
2 Pe 1:13	But I consider [it] right, for as long as I am in this habitation, to stir you up by a reminder,
2 Pe 1:14	[because I]<note: *Here "[because]" is supplied as a component of the participle ("know") which is understood as causal> know that the removal of my habitation is imminent, as indeed our Lord Jesus Christ made clear to me.
2 Pe 1:15	And I will also make every effort [that] you are able at any time, after my departure, {to recall these things to mind}<note: Literally "to make recollection of these">. 

2 Pe 1:16	For we did not make known to you the power and coming of our Lord Jesus Christ [by]<note: *Here "[by]" is supplied as a component of the participle ("following") which is understood as means> following ingeniously concocted myths, but [by]<note: *Here "[by]" is supplied as a component of the participle ("being") which is understood as means> being eyewitnesses of that one's majesty.
2 Pe 1:17	For [he] received honor and glory from God the Father [when]<note: *Here "[when]" is supplied as a component of the temporal genitive absolute participle ("was brought")> a voice such as this was brought to him by the Majestic Glory, "This is my beloved Son, in whom I am well pleased."
2 Pe 1:18	And [we] ourselves heard this voice brought from heaven [when we]<note: *Here "[when]" is supplied as a component of the participle ("were") which is understood as temporal> were with him on the holy mountain,
2 Pe 1:19	and we possess [as] more reliable the prophetic word, to which you do well [if you]<note: *Here "[if]" is supplied as a component of the participle ("pay attention to") which is understood as conditional> pay attention to [it] as to a lamp shining in a dark place, until the day dawns and the morning star rises in your hearts,
2 Pe 1:20	recognizing this above all, that every prophecy of scripture does not come about from one's own interpretation,
2 Pe 1:21	for no prophecy was ever produced by the will of man, but men carried along by the Holy Spirit spoke from God. 


CHAPTER 2
2 Pe 2:1	But there were also false prophets among the people, as there will be false teachers among you also, who will bring in {destructive heresies}<note: Literally "heresies of destruction">, even denying the Master who bought them, [thus]<note: *Here "[thus]" is supplied as a component of the participle ("bringing on") which is understood as result> bringing on themselves swift destruction.
2 Pe 2:2	And many will follow their licentious ways, because of whom the way of truth will be reviled.
2 Pe 2:3	And in greediness they will exploit you with false words, whose condemnation [from] long ago is not idle, and their destruction is not asleep. 

2 Pe 2:4	For if God did not spare the angels who sinned, but held [them] captive in Tartarus with chains of darkness [and] handed [them] over to be kept for judgment,
2 Pe 2:5	and did not spare the ancient world, but preserved Noah, a proclaimer of righteousness, {and seven others}<note: Literally "eighth"> [when he]<note: *Here "[when]" is supplied as a component of the participle ("brought") which is understood as temporal> brought a flood on the world of the ungodly,
2 Pe 2:6	and condemned the cities of Sodom and Gomorrah to destruction, reducing them to ashes, having appointed [them] [as] an example for those who are going to be ungodly,
2 Pe 2:7	and rescued righteous Lot, worn down by the way of life of lawless persons in licentiousness
2 Pe 2:8	(for that righteous man, [as he]<note: *Here "[as]" is supplied as a component of the participle ("lived") which is understood as temporal> lived among them day after day, was tormenting [his] righteous soul by the lawless deeds [he was] seeing and hearing),
2 Pe 2:9	[then] the Lord knows how to rescue the godly from trials and to reserve the unrighteous to be punished at<note: Or "until"> the day of judgment,
2 Pe 2:10	and especially those who go after the flesh in defiling lust<note: Literally "in lust of defilement," translated here as an attributive genitive> and who despise authority. 
 Bold [and] arrogant, they do not tremble in awe [as they]<note: *Here "[as]" is supplied as a component of the participle ("blaspheme") which is understood as temporal> blaspheme majestic beings,
2 Pe 2:11	whereas angels, who are greater in strength and power, do not bring against them a demeaning judgment.<note: Some manuscripts have "a demeaning judgment from the Lord">
2 Pe 2:12	But these persons, like irrational animals born [only with] natural [instincts] for capture and killing, blaspheming {about things}<note: Literally "with reference to which"> they do not understand, in their destruction will also be destroyed,
2 Pe 2:13	being harmed [as the] wages of unrighteousness. Considering reveling in the daytime a pleasure, [they are] stains and blemishes, carousing in their deceitful pleasures [when they]<note: *Here "[when]" is supplied as a component of the participle ("feast together") which is understood as temporal> feast together with you,
2 Pe 2:14	having eyes full of [desire for] an adulteress and unceasing from sin, enticing unstable persons, [and]<note: *Here "[and]" is supplied in keeping with English style> having hearts trained for greediness. Accursed children!
2 Pe 2:15	[By]<note: *Here "[by]" is supplied as a component of the participle ("leaving") which is understood as means> leaving the straight path, they have gone astray, [because they]<note: *Here "[because]" is supplied as a component of the participle ("followed") which is understood as causal> followed the way of Balaam the [son of] Bosor,<note: Although some English versions use "Beor" here, this is due to harmonization with the Old Testament; the vast majority of Greek manuscripts read "Bosor" here> who loved the wages of unrighteousness,
2 Pe 2:16	but received a rebuke for his own lawlessness: a speechless donkey, speaking with a human voice, restrained {the prophet's madness}<note: Literally "the of the prophet madness">. 

2 Pe 2:17	These [people] are waterless springs and mists driven by a hurricane, for whom the gloom of darkness has been reserved.
2 Pe 2:18	{For by speaking high-sounding but empty words}<note: Literally "for speaking pompous [words] of emptiness">, they entice with desires of the flesh [and] with licentiousness those who are scarcely escaping from those who live in error,
2 Pe 2:19	promising them freedom [although they]<note: *Here "[although]" is supplied as a component of the participle ("are") which is understood as concessive> themselves are slaves of depravity. For to whatever someone succumbs, by this he is also<note: Some manuscripts omit "also"> enslaved.
2 Pe 2:20	For if, [after they]<note: *Here "[after]" is supplied as a component of the participle ("have escaped from") which is understood as temporal> have escaped from the defilements of the world through the knowledge of the Lord<note: Some manuscripts have "of our Lord"> and Savior Jesus Christ, and they are again entangled in these [things] [and] succumb to [them], the last [state] has become worse for them than the first.
2 Pe 2:21	For it would have been better for them not to have known the way of righteousness than having known [it], to turn back from the holy commandment that had been delivered to them.
2 Pe 2:22	The [statement] of the true proverb has happened to them, "A dog returns to its own vomit,"<note: A paraphrased quotation from Prov 26:11> and "A sow, [after]<note: *Here "[after]" is supplied as a component of the participle ("washing herself") which is understood as temporal> washing herself, [returns]<note: *The verb "[returns]" is not in the Greek text, but is an understood repetition from the previous clause> to wallowing in the mud."<note: The source of this quotation is uncertain> 


CHAPTER 3
2 Pe 3:1	Dear friends, this [is] already the second letter I am writing to you, in [both of] which I am attempting to stir up your sincere mind by a reminder,
2 Pe 3:2	to remember the words proclaimed beforehand by the holy prophets and the commandment of the Lord and Savior through your apostles,
2 Pe 3:3	above all knowing this, that in the last days scoffers will come with scoffing, following according to their own desires
2 Pe 3:4	and saying, "Where is the promise of his coming? For {ever since}<note: Literally "from which [time]"> the fathers fell asleep, all [things] have continued just as they have been from the beginning of creation."
2 Pe 3:5	For [when]<note: *Here "[when]" is supplied as a component of the participle ("maintain") which is understood as temporal> they maintain this, it escapes [their] notice that the heavens existed long ago and the earth held together out of water and through water by the word of God,
2 Pe 3:6	by means of which things the world that existed at that time was destroyed [by]<note: *Here "[by]" is supplied as a component of the participle ("being inundated") which is understood as means> being inundated with water.
2 Pe 3:7	But by the same word the present heavens and earth are reserved for fire, being kept for the day of judgment and destruction of ungodly people. 

2 Pe 3:8	Now, dear friends, do not let this one thing escape your [notice], that one day with the Lord [is] like a thousand years, and a thousand years [is] like one day.
2 Pe 3:9	The Lord is not delaying the promise, as some consider slowness, but is being patient toward you, [because he]<note: *Here "[because]" is supplied as a component of the participle ("want") which is understood as causal> does not want any to perish, but all to come to repentance.
2 Pe 3:10	But the day of the Lord will come like a thief, in which the heavens will disappear with a rushing noise, and the celestial bodies will be destroyed [by]<note: *Here "[by]" is supplied as a component of the participle ("being burned up") which is understood as means> being burned up, and the earth and the deeds [done] on it will be disclosed.
2 Pe 3:11	[Because]<note: *Here "[because]" is supplied as a component of the participle ("are being destroyed") which is understood as causal> all these things are being destroyed in this way, what sort of [people] must you be in holy behavior and godliness,
2 Pe 3:12	[while]<note: *Here "[while]" is supplied as a component of the participle ("waiting for") which is understood as temporal> waiting for and hastening the coming of the day of God, because of which the heavens will be destroyed [by]<note: *Here "[by]" is supplied as a component of the participle ("being burned up") which is understood as means> being burned up and the celestial bodies will melt [as they]<note: *Here "[as]" is supplied as a component of the participle ("are consumed by heat") which is understood as temporal> are consumed by heat!
2 Pe 3:13	But according to his promise, we are waiting for new heavens and a new earth in which righteousness resides. 

2 Pe 3:14	Therefore, dear friends, [because you]<note: *Here "[because]" is supplied as a component of the participle ("are waiting for") which is understood as causal> are waiting for these [things], make every effort to be found at peace, spotless and unblemished in him.
2 Pe 3:15	And regard the patience of our Lord as salvation, just as also our dear brother Paul wrote to you, according to the wisdom that was given to him,
2 Pe 3:16	as [he does] also in all his<note: *Literally "the"; the Greek article is used here as a possessive pronoun><note: Some manuscripts do not explicitly state "his"> letters, speaking in them about these [things], in which there are some [things] hard to understand, which the ignorant and unstable distort to their own destruction, as [they] also [do] the rest of the scriptures.
2 Pe 3:17	Therefore, dear friends, [because you]<note: *Here "[because]" is supplied as a component of the participle ("know beforehand") which is understood as causal> know [this] beforehand, guard yourselves so that you do not lose your own safe position [because you]<note: *Here "[because]" is supplied as a component of the participle ("have been led away") which is understood as causal> have been led away by the error of lawless persons.
2 Pe 3:18	But grow in the grace and knowledge of our Lord and Savior Jesus Christ. To him [be] the glory, both now and to the day of eternity. Amen. 


----------------------------------------------------------------------------------------------
1 JOHN
----------------------------------------------------------------------------------------------
1 Jn	The First Letter of
 John

CHAPTER 1
1 Jn 1:1	What was from the beginning, what we have heard, what we have seen with our eyes, what we have looked at and our hands have touched, concerning the word of life--
1 Jn 1:2	and the life was revealed, and we have seen and testify and announce to you the eternal life which was with the Father and was revealed to us--
1 Jn 1:3	what we have seen and heard, we announce to you also, in order that you also may have fellowship with us, and indeed our fellowship [is] with the Father and with his Son Jesus Christ.
1 Jn 1:4	And these [things] we write, in order that our joy may be complete. 

1 Jn 1:5	And this is the message which we have heard from him and announce to you, that God is light and there [is] no darkness in him at all.
1 Jn 1:6	If we say that we have fellowship with him and walk in the darkness, we lie and do not practice the truth.<note: Or "we are lying and are not practicing the truth">
1 Jn 1:7	But if we walk in the light as he is in the light, we have fellowship with one another, and the blood of Jesus his Son cleanses us from all sin.
1 Jn 1:8	If we say that we do not have sin, we deceive ourselves and the truth is not in us.
1 Jn 1:9	If we confess our sins, he is faithful and just, so that he will forgive us [our]<note: *Literally "the"; the Greek article is used here as a possessive pronoun> sins and will cleanse us from all unrighteousness.
1 Jn 1:10	If we say that we have not sinned, we make him a liar, and his word is not in us. 


CHAPTER 2
1 Jn 2:1	My little children, I am writing these [things] to you in order that you may not sin. And if anyone sins, we have an advocate with the Father, Jesus Christ the righteous [one],
1 Jn 2:2	and he<note: Or "he himself" (emphatic)> is the propitiation<note: Or "expiation"; or "atoning sacrifice"> for our sins, and not for ours only, but also for [the sins of] the whole world.
1 Jn 2:3	And by this we know that we have come to know him, if we keep his commandments.
1 Jn 2:4	The one who says "I have come to know him," and does not keep his commandments is a liar, and the truth is not in this person.
1 Jn 2:5	But whoever keeps his word, truly in this person the love of God has been perfected. By this we know that we are in him.
1 Jn 2:6	The one who says [that he] resides in him ought also to walk<note: Some manuscripts have "to walk in this way"> just as that one walked. 

1 Jn 2:7	Dear friends, I am not writing a new commandment to you, but an old commandment which you have had from the beginning. The old commandment is the message which you have heard.
1 Jn 2:8	Again, I am writing a new commandment to you, which is true in him and in you, because<note: Or perhaps "that"> the darkness is passing away and the true light already is shining.
1 Jn 2:9	The one who says [he] is in the light and hates his brother is in the darkness until now.
1 Jn 2:10	The one who loves his brother resides in the light, and [there] is no cause for stumbling in him.
1 Jn 2:11	But the one who hates his brother is in the darkness, and walks in the darkness, and does not know where he is going, because the darkness has blinded his eyes. 

1 Jn 2:12	I am writing to you, little children, because<note: Or "that"> your sins have been forgiven you on account of his name.
1 Jn 2:13	I am writing to you, fathers, because<note: Or "that"> you have known the [One who is] from the beginning. I am writing to you, young men, because<note: Or "that"> you have conquered the evil one.
1 Jn 2:14	I have written to you, children, because<note: Or "that"> you have known the Father. I have written to you, fathers, because<note: Or "that"> you have known the [One who is] from the beginning. I have written to you, young men, because<note: Or "that"> you are strong, and the word of God resides in you, and you have conquered the evil one. 

1 Jn 2:15	Do not love the world or the things in the world. If anyone loves the world, the love of the Father is not in him,
1 Jn 2:16	because everything [that is] in the world--the desire of the flesh and the desire of the eyes and the arrogance of material possessions--is not from the Father, but is from the world.
1 Jn 2:17	And the world is passing away, and its desire,<note: Or "and the desire for it"> but the one who does the will of God remains {forever}<note: Literally "for the age">. 

1 Jn 2:18	Children, it is the last hour, and just as you have heard that antichrist is coming, even now many antichrists have arisen, by which we know that it is the last hour.
1 Jn 2:19	They went out from us, but they were not of us; for if they had been of us, they would have remained with us. But [they went out]<note: *This is an understood repetition of the phrase "they went out" from the beginning of v. 19>, in order that it might be shown that all of them are not of us. 

1 Jn 2:20	And you have an anointing from the Holy One, and you all know.
1 Jn 2:21	I have not written to you because<note: Or "that"> you do not know the truth, but because<note: Or "that"> you do know it, and because<note: Or "that"> every lie is not of the truth.
1 Jn 2:22	Who is the liar except the one who denies that Jesus is the Christ? This person is the antichrist, the one who denies the Father and the Son.
1 Jn 2:23	Everyone who denies the Son does not have the Father [either]; the one who confesses the Son has the Father also. 

1 Jn 2:24	[As for] you, what you have heard from the beginning must remain in you. If what you have heard from the beginning remains in you, you also will remain in the Son and in the Father.
1 Jn 2:25	And this is the promise which he himself promised us: eternal life.
1 Jn 2:26	These [things] I have written to you concerning the ones who are trying to deceive you. 

1 Jn 2:27	And [as for] you, the anointing which you received from him remains in you, and you do not have need that anyone teach you. But as his anointing teaches you about all [things], and is true and is not a lie, and just as it has taught you, you reside<note: *By form the verb could also be imperative: "just as it has taught you, reside in him"> in him. 

1 Jn 2:28	And now, little children, remain in him, so that whenever he is revealed we may have confidence and not be put to shame before him at his coming.
1 Jn 2:29	If you know that he is righteous, you know that everyone<note: Some manuscripts have "everyone also"> who practices righteousness has been fathered by him. 



"""

print(verses_followed_by_blank_line(text))