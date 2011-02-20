from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Poll import Poll

class SmartInfo(Poll, Converter, object):
	SMART_INFO_H = 0
	ORB_INFO = 1
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.type = {
				"ExpertInfo": self.SMART_INFO_H,
				"ExpertInfo_OrbPos": self.ORB_INFO,
			}[type]
		self.poll_interval = 10000
		self.poll_enabled = True
		self.ar_fec = ["Auto", "1/2", "2/3", "3/4", "5/6", "7/8", "3/5", "4/5", "8/9", "9/10","None","None","None","None","None"]
		self.ar_pol = ["H", "V", "CL", "CR", "na", "na", "na", "na", "na", "na", "na", "na"]

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""	
		Ret_Text1 = ""
		Ret_Text2 = ""
		Sec_Text = ""
		if (self.type == self.SMART_INFO_H): # HORIZONTAL
			decID = ""
			decCI = "0x000"
			decFrom = ""
			eMasTime = ""
			res = ""
			dccmd = ""
			searchIDs = []
			foundIDs = []
			feinfo = (service and service.frontendInfo())
			if (feinfo is not None):
				frontendData = (feinfo and feinfo.getAll(True))
				if (frontendData is not None):
					if ((frontendData.get("tuner_type") == "DVB-S") or (frontendData.get("tuner_type") == "DVB-C")):
						frequency = (str((frontendData.get("frequency") / 1000)) + " MHz")
						symbolrate = (str((frontendData.get("symbol_rate") / 1000)) + "")
						try:
							if (frontendData.get("tuner_type") == "DVB-S"):
								polarisation_i = frontendData.get("polarization")
							else:
								polarisation_i = 0
							fec_i = frontendData.get("fec_inner")
							Ret_Text1 = Ret_Text1 + frequency + "  " + self.ar_pol[polarisation_i] + "  " + self.ar_fec[fec_i] + "  " + symbolrate + " "
						except:
							Ret_Text1 = Ret_Text1 + frequency + " " + symbolrate + " "
						orb_pos = ""
						if (frontendData.get("tuner_type") == "DVB-S"):
							orbital_pos = int(frontendData["orbital_position"])
							if orbital_pos > 1800:
								if orbital_pos == 3590:
									orb_pos = 'Thor/Intelsat'
								elif orbital_pos == 3560:
									orb_pos = 'Amos (4'
								elif orbital_pos == 3550:
									orb_pos = 'Atlantic Bird'
								elif orbital_pos == 3530:
									orb_pos = 'Nilesat/Atlantic Bird'
								elif orbital_pos == 3520:
									orb_pos = 'Atlantic Bird'
								elif orbital_pos == 3475:
									orb_pos = 'Atlantic Bird'
								elif orbital_pos == 3460:
									orb_pos = 'Express'
								elif orbital_pos == 3450:
									orb_pos = 'Telstar'
								elif orbital_pos == 3420:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3380:
									orb_pos = 'Nss'
								elif orbital_pos == 3355:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3325:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3300:
									orb_pos = 'Hispasat'
								elif orbital_pos == 3285:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3170:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3150:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3070:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3045:
									orb_pos = 'Intelsat'
								elif orbital_pos == 3020:
									orb_pos = 'Intelsat 9'
								elif orbital_pos == 2990:
									orb_pos = 'Amazonas'
								elif orbital_pos == 2900:
									orb_pos = 'Star One'
								elif orbital_pos == 2880:
									orb_pos = 'AMC 6 (72'
								elif orbital_pos == 2875:
									orb_pos = 'Echostar 6'
								elif orbital_pos == 2860:
									orb_pos = 'Horizons'
								elif orbital_pos == 2810:
									orb_pos = 'AMC5'
								elif orbital_pos == 2780:
									orb_pos = 'NIMIQ 4'
								elif orbital_pos == 2690:
									orb_pos = 'NIMIQ 1'
								elif orbital_pos == 3592:
									orb_pos = 'Thor/Intelsat'
								elif orbital_pos == 2985:
									orb_pos = 'Echostar 3,12'
								elif orbital_pos == 2830:
									orb_pos = 'Echostar 8'
								elif orbital_pos == 2630:
									orb_pos = 'Galaxy 19'
								elif orbital_pos == 2500:
									orb_pos = 'Echostar 10,11'
								elif orbital_pos == 2502:
									orb_pos = 'DirectTV 5'
								elif orbital_pos == 2410:
									orb_pos = 'Echostar 7 Anik F3'
								elif orbital_pos == 2391:
									orb_pos = 'Galaxy 23'
								elif orbital_pos == 2390:
									orb_pos = 'Echostar 9'
								elif orbital_pos == 2412:
									orb_pos = 'DirectTV 7S'
								elif orbital_pos == 2310:
									orb_pos = 'Galaxy 27'
								elif orbital_pos == 2311:
									orb_pos = 'Ciel 2'
								elif orbital_pos == 2120:
									orb_pos = 'Echostar 2'
								else:
									orb_pos = str((float(3600 - orbital_pos))/10.0) + "W"
							elif orbital_pos > 0:
								if orbital_pos == 192:
									orb_pos = 'Astra 1F'
								elif orbital_pos == 130:
									orb_pos = 'Hot Bird 6,7A,8'
								elif orbital_pos == 235:
									orb_pos = 'Astra 1E'
								elif orbital_pos == 1100:
									orb_pos = 'BSat 1A,2A'
								elif orbital_pos == 1101:
									orb_pos = 'N-Sat 110'
								elif orbital_pos == 1131:
									orb_pos = 'KoreaSat 5'
								elif orbital_pos == 1440:
									orb_pos = 'SuperBird 7,C2'
								elif orbital_pos == 1006:
									orb_pos = 'AsiaSat 2'
								elif orbital_pos == 1030:
									orb_pos = 'Express A2'
								elif orbital_pos == 1056:
									orb_pos = 'Asiasat 3S'
								elif orbital_pos == 1082:
									orb_pos = 'NSS 11'
								elif orbital_pos == 881:
									orb_pos = 'ST1'
								elif orbital_pos == 900:
									orb_pos = 'Yamal 201'
								elif orbital_pos == 917:
									orb_pos = 'Mesat'
								elif orbital_pos == 950:
									orb_pos = 'Insat 4B'
								elif orbital_pos == 951:
									orb_pos = 'NSS 6'
								elif orbital_pos == 765:
									orb_pos = 'Telestar'
								elif orbital_pos == 785:
									orb_pos = 'ThaiCom 5'
								elif orbital_pos == 800:
									orb_pos = 'Express'
								elif orbital_pos == 830:
									orb_pos = 'Insat 4A'
								elif orbital_pos == 850:
									orb_pos = 'Intelsat 709'
								elif orbital_pos == 750:
									orb_pos = 'Abs'
								elif orbital_pos == 720:
									orb_pos = 'Intelsat'
								elif orbital_pos == 705:
									orb_pos = 'Eutelsat W5'
								elif orbital_pos == 685:
									orb_pos = 'Intelsat'
								elif orbital_pos == 620:
									orb_pos = 'Intelsat 902'
								elif orbital_pos == 600:
									orb_pos = 'Intelsat 904'
								elif orbital_pos == 570:
									orb_pos = 'Nss'
								elif orbital_pos == 530:
									orb_pos = 'Express AM22'
								elif orbital_pos == 480:
									orb_pos = 'Eutelsat 2F2'
								elif orbital_pos == 450:
									orb_pos = 'Intelsat'
								elif orbital_pos == 420:
									orb_pos = 'Turksat 2A'
								elif orbital_pos == 400:
									orb_pos = 'Express AM1'
								elif orbital_pos == 390:
									orb_pos = 'Hellas Sat 2'
								elif orbital_pos == 380:
									orb_pos = 'Paksat 1'
								elif orbital_pos == 360:
									orb_pos = 'Eutelsat Sesat'
								elif orbital_pos == 335:
									orb_pos = 'Astra 1M'
								elif orbital_pos == 330:
									orb_pos = 'Eurobird 3'
								elif orbital_pos == 328:
									orb_pos = 'Galaxy 11'
								elif orbital_pos == 315:
									orb_pos = 'Astra 5A'
								elif orbital_pos == 310:
									orb_pos = 'Turksat'
								elif orbital_pos == 305:
									orb_pos = 'Arabsat'
								elif orbital_pos == 285:
									orb_pos = 'Eurobird 1'
								elif orbital_pos == 284:
									orb_pos = 'Eurobird/Astra'
								elif orbital_pos == 282:
									orb_pos = 'Eurobird/Astra'
								elif orbital_pos == 1220:
									orb_pos = 'AsiaSat'
								elif orbital_pos == 1380:
									orb_pos = 'Telstar 18'
								elif orbital_pos == 260:
									orb_pos = 'Badr 3/4'
								elif orbital_pos == 255:
									orb_pos = 'Eurobird 2'
								elif orbital_pos == 215:
									orb_pos = 'Eutelsat'
								elif orbital_pos == 216:
									orb_pos = 'Eutelsat W6'
								elif orbital_pos == 210:
									orb_pos = 'AfriStar 1'
								elif orbital_pos == 160:
									orb_pos = 'Eutelsat W2'
								elif orbital_pos == 100:
									orb_pos = 'Eutelsat W1'
								elif orbital_pos == 90:
									orb_pos = 'Eurobird 9' 
								elif orbital_pos == 70:
									orb_pos = 'Eutelsat W3A'
								elif orbital_pos == 50:
									orb_pos = 'Sirius 4'
								elif orbital_pos == 48:
									orb_pos = 'Sirius 4'
								elif orbital_pos == 30:
									orb_pos = 'Telecom 2'
								else:
									orb_pos = str((float(orbital_pos))/10.0) + "E"
						Ret_Text1 = Ret_Text1 + "" + orb_pos
					elif (frontendData.get("tuner_type") == "DVB-T"):
						frequency = (str((frontendData.get("frequency") / 1000)) + " MHz")
						Ret_Text1 = Ret_Text1 + "Frequency: " + frequency
				prvd = info.getInfoString(iServiceInformation.sProvider)
				Ret_Text1 = prvd + "\n" + Ret_Text1
			res = ""
			Ret_Text1 = Ret_Text1
			return Ret_Text1

		if (self.type == self.ORB_INFO): # HORIZONTAL
			decID = ""
			decCI = "0x000"
			decFrom = ""
			eMasTime = ""
			res = ""
			dccmd = ""
			searchIDs = []
			foundIDs = []
			feinfo = (service and service.frontendInfo())
			if (feinfo is not None):
				frontendData = (feinfo and feinfo.getAll(True))
				if (frontendData is not None):
					if (frontendData.get("tuner_type") == "DVB-S"):
						orb_pos = ""
						if (frontendData.get("tuner_type") == "DVB-S"):
							orbital_pos = int(frontendData["orbital_position"])
							if orbital_pos > 1800:
								if orbital_pos == 3590:
									orb_pos = '1.0W'
								elif orbital_pos == 3560:
									orb_pos = '4.0W'
								elif orbital_pos == 3550:
									orb_pos = '5.0W'
								elif orbital_pos == 3530:
									orb_pos = '7.0W'
								elif orbital_pos == 3520:
									orb_pos = '8.0W'
								elif orbital_pos == 3475:
									orb_pos = '12.5W'
								elif orbital_pos == 3460:
									orb_pos = '14.0W'
								elif orbital_pos == 3450:
									orb_pos = '15.0W'
								elif orbital_pos == 3420:
									orb_pos = '18.0W'
								elif orbital_pos == 3380:
									orb_pos = '22.0W'
								elif orbital_pos == 3355:
									orb_pos = '24.5W'
								elif orbital_pos == 3325:
									orb_pos = '27.5W'
								elif orbital_pos == 3300:
									orb_pos = '30.0W'
								elif orbital_pos == 3285:
									orb_pos = '31.5W'
								elif orbital_pos == 3170:
									orb_pos = '43.0W'
								elif orbital_pos == 3150:
									orb_pos = '45.0W'
								elif orbital_pos == 3070:
									orb_pos = '53.0W'
								elif orbital_pos == 3045:
									orb_pos = '55.5W'
								elif orbital_pos == 3020:
									orb_pos = '58.0W'
								elif orbital_pos == 2990:
									orb_pos = '61.0W'
								elif orbital_pos == 2900:
									orb_pos = '0.0W'
								elif orbital_pos == 2880:
									orb_pos = '72.0W'
								elif orbital_pos == 2875:
									orb_pos = '72.7W'
								elif orbital_pos == 2860:
									orb_pos = '74.0W'
								elif orbital_pos == 2810:
									orb_pos = '79.0W'
								elif orbital_pos == 2780:
									orb_pos = '82.0W'
								elif orbital_pos == 2690:
									orb_pos = '91.0W'
								elif orbital_pos == 3592:
									orb_pos = '0.8W'
								elif orbital_pos == 2985:
									orb_pos = '61.5W'
								elif orbital_pos == 2830:
									orb_pos = '77.0W'
								elif orbital_pos == 2630:
									orb_pos = '97.0W'
								elif orbital_pos == 2500:
									orb_pos = '110.0W'
								elif orbital_pos == 2502:
									orb_pos = '110.0W'
								elif orbital_pos == 2410:
									orb_pos = '119.0W'
								elif orbital_pos == 2391:
									orb_pos = '121.0W'
								elif orbital_pos == 2390:
									orb_pos = '121.0W'
								elif orbital_pos == 2412:
									orb_pos = '119.0W'
								elif orbital_pos == 2310:
									orb_pos = '129.0W'
								elif orbital_pos == 2311:
									orb_pos = '129.0W'
								elif orbital_pos == 2120:
									orb_pos = '148.0W'
								else:
									orb_pos = str((float(3600 - orbital_pos))/10.0) + "W"
							elif orbital_pos > 0:
								if orbital_pos == 192:
									orb_pos = '19.2E'
								elif orbital_pos == 130:
									orb_pos = '13.0E'
								elif orbital_pos == 235:
									orb_pos = '23.5E'
								elif orbital_pos == 1100:
									orb_pos = '110.0E'
								elif orbital_pos == 1101:
									orb_pos = '110.0E'
								elif orbital_pos == 1131:
									orb_pos = '113.0E'
								elif orbital_pos == 1440:
									orb_pos = '144.0E'
								elif orbital_pos == 1006:
									orb_pos = '100.5E'
								elif orbital_pos == 1030:
									orb_pos = '103.0E'
								elif orbital_pos == 1056:
									orb_pos = '105.5E'
								elif orbital_pos == 1082:
									orb_pos = '108.2E'
								elif orbital_pos == 881:
									orb_pos = '88.0E'
								elif orbital_pos == 900:
									orb_pos = '90.0E'
								elif orbital_pos == 917:
									orb_pos = '91.5E'
								elif orbital_pos == 950:
									orb_pos = '95.0E'
								elif orbital_pos == 951:
									orb_pos = '95.0E'
								elif orbital_pos == 765:
									orb_pos = '76.5E'
								elif orbital_pos == 785:
									orb_pos = '78.5E'
								elif orbital_pos == 800:
									orb_pos = '80.0E'
								elif orbital_pos == 830:
									orb_pos = '83.0E'
								elif orbital_pos == 850:
									orb_pos = '85.2E'
								elif orbital_pos == 750:
									orb_pos = '75.0E'
								elif orbital_pos == 720:
									orb_pos = '72.0E'
								elif orbital_pos == 705:
									orb_pos = '70.5E'
								elif orbital_pos == 685:
									orb_pos = '68.5E'
								elif orbital_pos == 620:
									orb_pos = '62.0E'
								elif orbital_pos == 600:
									orb_pos = '60.0E'
								elif orbital_pos == 570:
									orb_pos = '57.0E'
								elif orbital_pos == 530:
									orb_pos = '53.0E'
								elif orbital_pos == 480:
									orb_pos = '48.0E'
								elif orbital_pos == 450:
									orb_pos = '45.0E'
								elif orbital_pos == 420:
									orb_pos = '42.0E'
								elif orbital_pos == 400:
									orb_pos = '40.0E'
								elif orbital_pos == 390:
									orb_pos = '39.0E'
								elif orbital_pos == 380:
									orb_pos = '38.0E'
								elif orbital_pos == 360:
									orb_pos = '36.0E'
								elif orbital_pos == 335:
									orb_pos = '33.5E'
								elif orbital_pos == 330:
									orb_pos = '33.0E'
								elif orbital_pos == 328:
									orb_pos = '32.8E'
								elif orbital_pos == 315:
									orb_pos = '31.5E'
								elif orbital_pos == 310:
									orb_pos = '31.0E'
								elif orbital_pos == 305:
									orb_pos = '30.5E'
								elif orbital_pos == 285:
									orb_pos = '28.5E'
								elif orbital_pos == 284:
									orb_pos = '28.4E'
								elif orbital_pos == 282:
									orb_pos = '28.2E'
								elif orbital_pos == 1220:
									orb_pos = '122.0E'
								elif orbital_pos == 1380:
									orb_pos = '138.0E'
								elif orbital_pos == 260:
									orb_pos = '26.0E'
								elif orbital_pos == 255:
									orb_pos = '25.5E'
								elif orbital_pos == 215:
									orb_pos = '21.5E'
								elif orbital_pos == 216:
									orb_pos = '21.6E'
								elif orbital_pos == 210:
									orb_pos = '21.0E'
								elif orbital_pos == 160:
									orb_pos = '16.0E'
								elif orbital_pos == 100:
									orb_pos = '10.0E'
								elif orbital_pos == 90:
									orb_pos = '9.0E' 
								elif orbital_pos == 70:
									orb_pos = '7.0E'
								elif orbital_pos == 50:
									orb_pos = '5.0E'
								elif orbital_pos == 48:
									orb_pos = '4.8E'
								elif orbital_pos == 30:
									orb_pos = '3.0E'
								else:
									orb_pos = str((float(orbital_pos))/10.0) + "E"
						Ret_Text2 = orb_pos

				#Ret_Text2 = prvd + "  " + Ret_Text2
			res = ""
			Ret_Text2 = Ret_Text2
			return Ret_Text2
		return ""

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)

	def kurz(self, langTxt):
		if (len(langTxt)>23):
			retT = langTxt[:20]+"..."
			return retT
		else:
			return langTxt
