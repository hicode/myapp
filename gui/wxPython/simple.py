import wx #1

class App(wx.App):#2

    def OnInit(self): #3
        frame = wx.Frame(parent=None, title='Bare')
        frame.Show()
        return True

app = App() #4
app.MainLoop() #5

'''
1. lonely  2. hero  3. yesterday  
4. yellow  5. complicated  6. my love  
7. all rise  8. thank you  9. big big world  
10. one love  11. casablanca  12. baby one more time  
13. here i am  14. because of you  15. yesterday once more  
16. right here waiting  17. in the end  18. seasons in the sun  
19. we will rock you  20. hotel california  21. god is a girl  
22. far away from home  23. without you  24. Wonderwall  
25. when you believe  26. as long as you love me  27. pretty boy  
28. shape of my heart  29. my heart will go on  30. loving you  
31. close to you  32. only time  33. Affirmation  
34. you raise me up  35. dying in the sun  36. no matter what  
37. Never say goodbye  38. anyone of us  39. just one last dance  
40. the day you went away  41. To be with you  42. Superstition  
43. i want it that way  44. the power of love  45. don't cry  
46. The call  47. i will always love you  48. better man  
49. heal the world  50. take me to your heart  51. moonlight shadow  
52. Smells like teen spirit  53. You are not alone  54. Top of the world  
55. Friday night  56. hey jude  57. say you say me  
58. rhythm of the rain  59. Larger than life  60. Try to remember  
61. Walk on  62. Mmmbop  63. i believe i can fly  
64. only love  65. tears in heaven  66. moon river  
67. unchained melody  68. Like a virgin  69. Only you  
70. Bye Bye Bye  71. Around the world  72. A thousand miles  
73. Mirror Mirror  74. Tonight I celebrate my love  75. For the love of God  
76. I will survive  77. Keep the faith  78. American life  
79. If God will send his angels  80. No scrubs  81. Colours of the wind  
82. All at once  83. When I dream  84. On my way home  
85. Little wing  86. Just my imagination   87. From me to you  
88. Tainted love  89. Rose garden   90. You are the sunshine of my life  
91. I want to know what love is   92. My generation   93. Green light  
94. Until you come back  95. Good vibrations  96. scarborough fair  
97. She bangs  98. Wish you were here  99. Like a rolling stone  
100. Genie in a bottle  101. Behind blue eyes  102. Alanis morissette  
103. Best In Me  104. Losing grip  105. Get the party started  
106. When a man loves a woman   107. Breaking My Heart  108. Bohemian rhapsody  
109. and life  110. End of the road  111. I want you back  
112. Dancing queen  113. With or without you  114. Love will keep us alive  
115. Kiss from a rose  116. Edelweiss   117. Now and forever  
118. The reason  119. Because you love me  120. Woman in love   
121. Can't Get You Out Of My Head  122. Yesterday once more   123. I will always love you   
124. Eternal flame  125. I Swear   126. Only love   
127. I believe I can fly   128. Moon river   129. Rhythm of the rain   
130. White flag  131. Careless whisper   132. Everything I do  
133. Promises don t come easy   134. All out Of Love   135. Gloomy sunday  
136. Unchained melody   137. Take me away  138. My prerogative  
139. If I let you go  140. How deep is your love   141. Never had a dream come true  
142. Billie jean  143. Rock with you  144. What a wonderful world  
145. Every breath you take  146. Flying without wings 
'''