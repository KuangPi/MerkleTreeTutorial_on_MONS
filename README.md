# Merkle Tree Tutorial on MONS
 <p>A practice code for Merkle Tree. </p>
 <p>The programmer of these codes are high school students. Please point it out if any format is inappropriate. </p>
 <p>My e-mail address is: qiaoyu.zhang@student.keystoneacademy.cn</p>

# How To Create a Merkle Tree for the MONS Project

<p>Before everything, let's make a list of all the features this Merkle Tree must include:</p>
<p>1. Read and Write a txt file and transfer the data in it into the program</p>
<p>2. Do hash. I prefer SHA256. </p>
<p>3. Should be able to verify the tree is valid. In other word, it must proof itself is a part of the Merkle Tree</p>
<p>4. Should be able to output the tree in some kinds of form.</p>

<br />

<p>So how should we achieve those?</p>

<p>2 is a relatively easy one. The only thing you need to do is import the python hash library and find its grammar.</p>
<p>And you will be fine.</p>
<p>But if you want to make the use of it easier, you could write a function to give it an unchanged argument.</p>
<p>And that is the way I did it.</p>

<br />

<p>1 could also be achieved by using the file library inside python.</p>
<p>But there is one thing need to be solved.</p>
<p>Since the txt file could be treat as a whole long string. What format should each tree use?</p>
<p>And that links to 4.</p>

<br />

<p>4's output should not be the same as 1. So possibility, repr and str method should be use at the same time. </p>
<p>Output of 4 should be readable. Currently, I'm studying pyqt5, so I decided to make it available in a GUI</p>

<br />

<p>Finally, here comes 3. The validation, which I believe is the hardest part. Details about its solution should be published at next updates. </p>

<br />
