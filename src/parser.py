# htmlのパーサーを描くぞ！
import os
import sys
import re



if __name__ == '__main__':
	listdirfile = os.listdir(path="../data/")
	listhtml = [i for i in listdirfile if i.find("html") != -1]

	list_title = []
	for ihtml in listhtml:
		with open("../data/"+ihtml) as f:
			lines = f.readlines()
			preline = ""
			# 変数
			name = ""
			media = ""
			time = -1
			country = ""
			info = ""
			day = ""
			list_genre = []
			eirin = ""
			directer = ""
			screenplayer = ""
			production = ""
			original = False
			music = ""
			list_acter = []
			# 作業用変数
			flag_actor = False

			for line in lines:
				# タイトル名
				if line.find("<h1 class=\"title\">") != -1:
					start = line.find("<h1 class=\"title\">")
					end = line.find("<span class=\"age\">")
					name = line[start+len("<h1 class=\"title\">"):end]
				# 上映時間
				if preline.find("td class=\"fwb\">上映時間") != -1:
					start = line.find("<td>")
					end = line.find("分")
					time = int(line[start+len("<td>"):end])
				# 製作国
				if preline.find("td class=\"fwb\">製作国") != -1:
					start = line.find("<td>")
					end = line.find("</td>")
					country = line[start+len("<td>"):end]
				# 公開情報
				if preline.find("td class=\"fwb\">公開情報") != -1:
					start = line.find("<td>")
					end = line.find("</td>")
					info = line[start+len("<td>"):end]
				# 初公開年月
				if preline.find("td class=\"fwb\">初公開年月") != -1:
					# なんか変なリンクが入ってるので、"<"~">"までを消しとばす
					day = re.sub("<.*?>", "", line)
					day = day.replace('\t',"")
					day = day.replace('\n',"")
				# ジャンル
				if preline.find("td class=\"fwb\">ジャンル") != -1:
					start = line.find("<td>")
					end = line.find("</td>")
					genre = line[start+len("<td>"):end]
					list_genre = genre.split("／")
				# 映倫
				if preline.find("td class=\"fwb\">映倫") != -1:
					start = line.find("<td>")
					end = line.find("</td>")
					eirin = line[start+len("<td>"):end]
				# 監督
				if preline.find("<td>監督") != -1:
					# なんか変なリンクが入ってるので、"<"~">"までを消しとばす
					directer = re.sub("<.*?>", "", line)
					directer = directer.replace('\t',"")
					directer = directer.replace('\n',"")
				# 脚本
				if preline.find("<td>脚本") != -1:
					# なんか変なリンクが入ってるので、"<"~">"までを消しとばす
					screenplayer = re.sub("<.*?>", "", line)
					screenplayer = screenplayer.replace('\t',"")
					screenplayer = screenplayer.replace('\n',"")
				# アニメーション製作(任意)
				if preline.find("<td>アニメーション") != -1:
					# なんか変なリンクが入ってるので、"<"~">"までを消しとばす
					production = re.sub("<.*?>", "", line)
					production = production.replace('\t',"")
					production = production.replace('\n',"")
				# 原作(任意)
				if preline.find("<td>原作") != -1:
					original = True
				# 音楽
				if preline.find("<td>音楽") != -1:
					# なんか変なリンクが入ってるので、"<"~">"までを消しとばす
					music = re.sub("<.*?>", "", line)
					music = music.replace('\t',"")
					music = music.replace('\n',"")
				# 出演/声の出演
				if preline.find("<td>出演") != -1 or preline.find("<td>声の出演") != -1:
					flag_actor = True
					# なんか変なリンクが入ってるので、"<"~">"までを消しとばす
					actor = re.sub("<.*?>", "", line)
					actor = actor.replace('\t',"")
					actor = actor.replace('\n',"")
					list_acter.append(actor)
				if flag_actor and preline.find("<td></td>") != -1:
					actor = re.sub("<.*?>", "", line)
					actor = actor.replace('\t',"")
					actor = actor.replace('\n',"")
					list_acter.append(actor)
				# 出演を閉じる
				if line.find("</tbody>") != -1:
					flag_actor = False

				preline = line

			list_title.append([name ,media ,time ,country ,info ,day ,list_genre ,eirin ,directer ,screenplayer ,production ,original ,music ,list_acter])


	with open("../data/output.csv", mode="w") as f:
		f.write("名前,メディア,上映時間,製作国,公開情報,公開年月日,ジャンル,映倫,監督,製作,アニメ製作,原作,音楽,出演\n")
		for title in list_title:
			for it in title:
				if type(it) is str:
					f.write(it)
					f.write(",")
				if type(it) is int:
					f.write(str(it))
					f.write(",")
				if type(it) is list:
					for j in it:
						f.write(j)
						f.write("_")
					f.write(",")
			f.write('\n')
