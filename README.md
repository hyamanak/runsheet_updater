<!-----

You have some errors, warnings, or alerts. If you are using reckless mode, turn it off to see inline alerts.
* ERRORs: 0
* WARNINGs: 0
* ALERTS: 9

Conversion time: 2.37 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β34
* Tue Sep 19 2023 23:41:25 GMT-0700 (PDT)
* Source doc: RunSheetの更新方法
* This document has images: check for >>>>>  gd2md-html alert:  inline image link in generated source and store images to your server. NOTE: Images in exported zip file from Google Docs may not appear in  the same order as they do in your doc. Please check the images!


WARNING:
You have 8 H1 headings. You may want to use the "H1 -> H2" option to demote all headings by one level.

----->


<p style="color: red; font-weight: bold">>>>>>  gd2md-html alert:  ERRORs: 0; WARNINGs: 1; ALERTS: 9.</p>
<ul style="color: red; font-weight: bold"><li>See top comment block for details on ERRORs and WARNINGs. <li>In the converted Markdown or HTML, search for inline alerts that start with >>>>>  gd2md-html alert:  for specific instances that need correction.</ul>

<p style="color: red; font-weight: bold">Links to alert messages:</p><a href="#gdcalert1">alert1</a>
<a href="#gdcalert2">alert2</a>
<a href="#gdcalert3">alert3</a>
<a href="#gdcalert4">alert4</a>
<a href="#gdcalert5">alert5</a>
<a href="#gdcalert6">alert6</a>
<a href="#gdcalert7">alert7</a>
<a href="#gdcalert8">alert8</a>
<a href="#gdcalert9">alert9</a>

<p style="color: red; font-weight: bold">>>>>> PLEASE check and correct alert issues and delete this message and the inline alerts.<hr></p>



# RunSheetの更新方法

スクリプトの入手、ファイルの準備ができていない場合は、[RunSheetUpdatorの使い方](https://docs.google.com/document/d/1VeUtS7RscGI2s5Ptvnb-eyyK443Ak6Lw6p1JBsJhPt4/edit)を参照してください。


# 準備

@l10n-jp チャンネルで更新することをアナウンスします。


# シートをロック

	RunsheetのDocumentation ページ上部のメニュー [Extensions] から [Macros] -> [LockSheet] をクリックします。すると、Documentation シートがロックされ、自分とボット以外の書き込みができなくなります。**スクリプトを実行するにあたって、警告が表示されることがあります**が、そのまま許可を選びます

	

<p id="gdcalert1" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image1.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert2">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image1.png "image_tooltip")



# バックアップを作成

	Documentationシートの逆三角アイコンをクリックして、[Duplicate] をクリックします。



<p id="gdcalert2" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image2.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert3">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image2.png "image_tooltip")


	すると、Documentation のコピーというシートが作成されるので、そのシートの名前を0905(月日)BackUp という名前に変更します。


# Notesシートを作成

	前日のNotesシートを再利用して、作業日のものを作ります。前回と同様、前日のNotesシートを右クリックし、 [Duplicate] をクリックします。次にコピーを作成して、更新日の日付+Notes (ex. 0905Notes) というシートを作ります。その後、前日の内容を削除しておきましょう。



<p id="gdcalert3" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image3.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert4">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image3.png "image_tooltip")



# スクリプト実行後のファイルから内容をコピー

スクリプト実行で生成された**updated_daily.csv**ファイルをテキストファイルで開きます。excelなどの表計算アプリは使わないようにしてください。

テキストエディターで開いた見た目はこんな感じです。



<p id="gdcalert4" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image4.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert5">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image4.png "image_tooltip")


	こちらをCtrl+a (cmd + a) ですべて選択して、Ctrl+c (cmd + c) でコピーしておきます。

ランシートのDocumentationシートに行き、A2に現在セルを移動します。



<p id="gdcalert5" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image5.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert6">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image5.png "image_tooltip")


そこで右クリックして[paste speciall] ->  [Value only] を選択します。すると、少し下の部分にクリップボードのアイコンが現れます。



<p id="gdcalert6" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image6.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert7">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image6.png "image_tooltip")


こちらをクリックして開き、[Split text to clumns] を選択します。



<p id="gdcalert7" ><span style="color: red; font-weight: bold">>>>>>  gd2md-html alert: inline image link here (to images/image7.png). Store image on your image server and adjust path/filename/extension if necessary. </span><br>(<a href="#">Back to top</a>)(<a href="#gdcalert8">Next alert</a>)<br><span style="color: red; font-weight: bold">>>>>> </span></p>


![alt_text](images/image7.png "image_tooltip")


すると、すべてのセルデータが新しいデータに置き換わります。


# nomatch.csvのコンテンツの追加

こちらのファイルの内容は、**updated_daily.csv**と同じ形式です。中身のデータは、現在のランシートに存在しないもので、デイリー更新で上がってきたものです。

こちらは、手動で確認して追加を行います。

まず、updated_daily.csvのときと同様に、CTRL + a と CTRL + c で内容をコピーします。続いて、Notesシートに行き、A2セルを選択してチェックします。




そして、右クリックで、daily_update.csvを貼り付けたときと同様、[value only]を選択肢、クリップボードアイコンで [Split text to clumns] を選択します。


# 仕上げ

いよいよ仕上げです


## セルの色を戻す

	一部の列は薄い灰色です。更新後はこれが解除されているので戻します。Documentationページに行き、上部のメニューから [Extension] -> [Macros] -> [Cell Color] をクリックします。すると....あるべき色になります。



## 日付形式を戻す

	データ更新を行うと、一部日付データ形式が乱れることがあります。色を戻す手順に従い、[FixDateFormat] をクリックします。


## 見積もりの数式を適用する

見積もり時間を正しい値にする積もり時間のL列には、数式が入っていま

	見す。これは毎回変更や追加があった場合に適用が必要になります。前回と同じ手順で、[hoursEst] を選択します。


## アドレスのハイパーリンクを修正する

	更新後は、ハイパーリンクが消えるものがあります。シート上部のメニューから [Edit] -> [Find and replace] を選択し、[Find] に https、[Replace with] に https を入力し、[Replace all] を押します。

	


# さいごに


## ロックを解除する

	ロックを行ったときと同じ手順に従い、[UnlockSheet] を選択すると、ロックが解除されます。


## アナウンスしておしまい

@l10n-jp に終わったことを伝えて、あなたの仕事はおしまいです。

おつかれさまでした
