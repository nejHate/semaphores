import subprocess
import re
import random

if 0: # ech nechce se mi to předělávat na komentáře xd
  print("tento program bude testovat korektnost výstupů. bude testovat okrajové hodnoty a následně náhodné hodnoty")
  print("zadejte hodnoty pro maximum procesů pro jeden typ (tzn. pokud dáte 20 tak se spustí 41 procesů")
  print("(main + 20 zákazníků + 20 úředníků) plus 1 proces bude tenhle skript")
  print("nwm zda python může běžet na merlinovi ale pokud to uděláte buďte na něj milí <3")
  print("pokud dojde k chybě program se ukončí a v project_tester.out bude poslední průběh testem")
  print("pokud v souboru objevíte řádek začínající \"error\" takse vstahuje k řádku nad tím")
  print("program vypíše vše co najde v proj2.out a popřípadně pod chybný řádek vloží errorovou hlášku")
  print("na konci souboru jsou vypsané řádky navíc")
  print("některé řádky obsahují array s nulama. to z toho důvodu že se jejich id přesunulo jinam")
  print("jediné řádky kde by měli být čísla jsou:")
  print("home zakaznici, home urednici, all zakaznici, all urednici a print order")
  print("wait zákazníci jsou zákazníci kteří vypsali \"starting\". samé nuly == good")
  print("ready úředníci jsou úředníci co napsali \"starting\". samé nuly == good")
  print("queue1 až 3 jsou \"přepážky\" kam vstoupili zákazníci a čekají na spracování")
  print("ready queue je číslo které značí počet zákazníků čekajících ve frontě. samé nuly == good")
  print("procesing zákazníci jsou zákazníci kteří napsali \"entering office for a service\". samé nuly == good")
  print("procesing úředníci jsou úředníci kteří vypsali \"serving a service of type\". samé nuly == good")
  print("sleeping urednici jsou urednici co vypsali \"taking break\". samé nuly == good")
  print("home zákazníci jsou zákazníci co napsali \"going home\". všechny id == good")
  print("home úředníci jsou úředníci co napsali \"going home\". všechny id == good")
  print("all zákazníci jsou všichni zákazníci (všichni co napsali \"started\". použito pro kontrolu na konci. všechny id == good")
  print("all úředníci jsou všichni úředníci (všichni co napsali \"started\". použito pro kontrolu na konci. všechny id == good")
  print("print order jsou čísla řádků popořadě jak se načítal soubor proj2.out. od 1 po N == good") # tohle se neprintuje je to moc dlouhé
  # pokud nemáte řádky popořadě srolujte nahoru. na začátku projec_tester.out je výpis řádků z proj2.out a jsou tam i errory vypsané
  print("další řádky jsou printy toho zda jsou předchozí řádky vypsané v pohodě")
  print("pokud něco není tak je někde chyba")
  print("pokud chybu nemáte a myslíte si že mám chybu u sebe tak mi pošlete project_tester.out a já to zkusím spravit")
  

repeat = int(input("zadejte kolik opakování chcete udělat, více = lépe xd: "))

max_threads = int(input("zadejte maximum thredů jednoho typu: "))

start_parametres = [[1, max_threads, 10, 10, 200],
                   [max_threads, 1, 10, 10, 200],
                   [max_threads, max_threads, 10, 10, 200],
                   [1, 1, 10, 10, 200],
                    
                   [1, max_threads, 0, 0, 200],
                   [max_threads, 1, 0, 0, 200],
                   [max_threads, max_threads, 0, 0, 200],
                   [1, 1, 0, 0, 200],
                    
                   [1, max_threads, 1, 1, 200],
                   [max_threads, 1, 1, 1, 200],
                   [max_threads, max_threads, 1, 1, 200],
                   [1, 1, 1, 1, 200],
                    
                   [1, max_threads, 1000, 100, 2000],
                   [max_threads, 1, 1000, 100, 2000],
                   [max_threads, max_threads, 1000, 100, 2000],
                   [1, 1, 1000, 100, 2000],
                   
                   [1, max_threads, 1000, 100, 0],
                   [max_threads, 1, 1000, 100, 0],
                   [max_threads, max_threads, 1000, 100, 0],
                   [1, 1, 1000, 100, 0]]
                    

for i in range(repeat):
  output = open("project_tester.out", "w")

  if(i < 20): # počet řádků argumentů start_parametres
    arg = start_parametres[i]
  else:
    arg[0] = random.randint(1, max_threads) #klidně si tu dejte *10 aby bylo zákazníků více
    arg[1] = random.randint(1, 10)
    arg[2] = random.randint(1, 1000) # klidně přepište
    arg[3] = random.randint(1, 100) # klidně přepište
    arg[4] = random.randint(1, 1000) # klidně přepište
    
  print(str(i) + ":", arg[0], arg[1], arg[2], arg[3], arg[4])
  
  #subprocess.call(["./proj2", str(arg[0]), str(arg[1]), str(arg[2]), str(arg[3]), str(arg[4])])

  wait_zakaznici = [0]
  
  ready_urednici = [0]
  
  queue1 = [0]
  queue2 = [0]
  queue3 = [0]
  
  ready_queue = [0, 0, 0]
  
  processing_zakaznici = [0]
  processing_urednici = [0]
  
  sleeping_urednici = [0]
  
  home_zakaznici = []
  home_urednici = []
  
  all_zakaznici = []
  all_urednici = []
  
  print_order = []

  linecounter = 0
  opened = 1
  error = 0
  
  regex = r"((\d*): Z (\d*): started)|((\d*): U (\d*): started)|((\d*): Z (\d*): entering office for a service (\d))|((\d*): U (\d*): serving a service of type (\d*))|((\d*): Z (\d*): called by office worker)|((\d*): U (\d*): service finished)|((\d*): Z (\d*): going home)|((\d*): U (\d*): taking break)|((\d*): U (\d*): break finished)|((\d*): closing)|((\d*): U (\d*): going home)"
  
  file = open("proj2.out", "r")
  test_str = file.read()
  
  matches = re.finditer(regex, test_str, re.MULTILINE)
  
  for matchNum, match in enumerate(matches, start=1):
  
    # zákazníci čekají
    # Z started
    if ((match.groups()[0]) != None):
      output.write(match.groups()[0] + "\n")
      if(int(match.groups()[1])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[1])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[1]))
      all_zakaznici.append(int(match.groups()[2]))
      wait_zakaznici.append(int(match.groups()[2]))
  
    # připravení úředníci
    # U started
    if ((match.groups()[3]) != None):
      output.write(match.groups()[3] + "\n")
      if(int(match.groups()[4])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[4])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[4]))
      all_urednici.append(int(match.groups()[5]))
      ready_urednici.append(int(match.groups()[5]))
  
    # waiting for one of three services
    if ((match.groups()[6]) != None):
      output.write(match.groups()[6] + "\n")
      if(int(match.groups()[7])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[7])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[7]))
      if opened == 1:
        if (int(match.groups()[8])) in wait_zakaznici:
          wait_zakaznici[wait_zakaznici.index(int(match.groups()[8]))] = 0
          if (int(match.groups()[9])-1) == 0:
            queue1.append(int(match.groups()[8]))
            ready_queue[0] += 1
          elif (int(match.groups()[9])-1) == 1:
            queue2.append(int(match.groups()[8]))
            ready_queue[1] += 1
          elif (int(match.groups()[9])-1) == 2:
            queue3.append(int(match.groups()[8]))
            ready_queue[2] += 1
          else:
            output.write("error zákazník se chce zařadit do fronty která neexistuje\n")
            error = 1
        else:
          output.write("error, zákazník se zařadil do fronty, ikdyž jeho předchozí stav nebyl waiting\n")
          error = 1
      else:
        output.write("error, pošta je zavřená takže zákazník se nemůže zařadit do fronty\n")
        error = 1
  
    # urednik jde spracovavat jednu z queue
    if ((match.groups()[10]) != None):
      output.write(match.groups()[10] + "\n")
      if(int(match.groups()[11])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[11])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[11]))
      if (int(match.groups()[12])) in ready_urednici:
        ready_urednici[ready_urednici.index(int(match.groups()[12]))] = 0
        processing_urednici.append(int(match.groups()[12]))
        ready_queue[int(match.groups()[13]) - 1] -= 1
      else:
        output.write("error, úředník se nenachází ve stavu, ve kterém se rozhoduje zda obsluhovat nebo jít spát\n")
        error = 1
  
    # zakaznik je spracovavan    
    if ((match.groups()[14]) != None):
      output.write(match.groups()[14] + "\n")
      if(int(match.groups()[15])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[15])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[15]))
      if (int(match.groups()[16])) in queue1:
        queue1[queue1.index(int(match.groups()[16]))] = 0
        processing_zakaznici.append(int(match.groups()[16]))
      elif (int(match.groups()[16])) in queue2:
        queue2[queue2.index(int(match.groups()[16]))] = 0
        processing_zakaznici.append(int(match.groups()[16]))
      elif (int(match.groups()[16])) in queue3:
        queue3[queue3.index(int(match.groups()[16]))] = 0
        processing_zakaznici.append(int(match.groups()[16]))
      else:
        output.write("error, nikdo neobsluhuje danou frontu\n")
        error = 1
  
    # urednik dokoncil praci a jde se zas pripravit
    if ((match.groups()[17]) != None):
      output.write(match.groups()[17] + "\n")
      if(int(match.groups()[18])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[18])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[18]))
      if (int(match.groups()[19])) in processing_urednici:
        processing_urednici[processing_urednici.index(int(match.groups()[19]))] = 0
        ready_urednici.append(int(match.groups()[19]))
      else:
        output.write("error, úředník právě nepracoval (klasika) a nemůže se proto připravit na další\n")
        error = 1
  
    # zakaznik jde dom chrupkat
    if ((match.groups()[20]) != None):
      output.write(match.groups()[20] + "\n")
      if(int(match.groups()[21])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[21])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[21]))
      if (int(match.groups()[22])) in processing_zakaznici:
        processing_zakaznici[processing_zakaznici.index(int(match.groups()[22]))] = 0
        home_zakaznici.append(int(match.groups()[22]))
      elif (int(match.groups()[22])) in wait_zakaznici:
        if opened == 0:
          wait_zakaznici[wait_zakaznici.index(int(match.groups()[22]))] = 0
          home_zakaznici.append(int(match.groups()[22]))
        else:
          output.write("error, pošta nejspíš není zavřená a zákazník šel domů\n")
          error = 1
      else:
        output.write("error, zákazník není ve spracováván úředníkem a zároveň je pošta otevřena\n")
        error = 1
  
    #urednik si jde schrupknout
    if ((match.groups()[23]) != None):
      output.write(match.groups()[23] + "\n")
      if(int(match.groups()[24])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[24])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[24]))
      if (int(match.groups()[25])) in ready_urednici:
        if max(ready_queue) == 0:
          ready_urednici[ready_urednici.index(int(match.groups()[25]))] = 0
          sleeping_urednici.append(int(match.groups()[25]))
        else:
          ready_urednici[ready_urednici.index(int(match.groups()[25]))] = 0
          sleeping_urednici.append(int(match.groups()[25]))
          output.write("error, úředník nemůže jít spát když je zákazník v queue\n")
          output.write("tento error se může objevit pokud kontrolujete stav fronty bez sem_wait() a např zkontroluje\n")
          output.write("frontu 1 a 2, zákazník vejde do fronty 1 apak úředník dokontroluje frontu 3 a jde spát\n")
          output.write("tuhle správu můžete klidně smazat (řádek 268 - 273 snad bo se to mění a já to nebudu pokaždé měnit ani řešit jak to udělat automaticky)\n")
          output.write("hlavně si odstraňte řádek kde je error = 1 jinak se vám to bude pořád ukončovat")
          error = 1 # tenhle řádek lze v nutnosti odstranit, v projektu se nebere jako chyba
      else:
        output.write("error, úředník si nemůže jít schrupnout, protože není ve fázi rozhodování\n")
        error = 1
  
    #urednik jde makat
    if ((match.groups()[26]) != None):
      output.write(match.groups()[26] + "\n")
      if(int(match.groups()[27])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[27])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[27]))
      if (int(match.groups()[28])) in sleeping_urednici:
        sleeping_urednici[sleeping_urednici.index(int(match.groups()[28]))] = 0
        ready_urednici.append(int(match.groups()[28]))
      else:
        output.write("error, úředník nemůže jít makat protože se nenachází v rozhodovací fázi zda makat nebo jít spát\n")
        error = 1
  
    # stejne nemakali tak se nic nemeni, closing
    if ((match.groups()[29]) != None):
      output.write(match.groups()[29] + "\n")
      if(int(match.groups()[30])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[30])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[30]))
      opened = 0
  
    # urednik jde chrupkat dom
    if ((match.groups()[31]) != None):
      output.write(match.groups()[31] + "\n")
      if(int(match.groups()[32])) == (linecounter + 1):
        linecounter += 1
      else:
        linecounter = int(match.groups()[32])
        output.write("error, řádky nejsou popořadě\n")
      print_order.append(int(match.groups()[32]))
      if opened == 0:
        if (int(match.groups()[33])) in ready_urednici:
          ready_urednici[ready_urednici.index(int(match.groups()[33]))] = 0
          home_urednici.append(int(match.groups()[33]))
        else:
          output.write("error, úředník nemůže jít domů, protože se nenachází v čekací frontě\n")
          error = 1
      else:
        output.write("error, úředník nemůže jít domů, protože pošta je stále otevřená\n")
        error = 1
  
  output.write("\nwait zakaznici {}\n".format(wait_zakaznici))
  output.write("ready urednici {}\n".format(ready_urednici))
  output.write("queue1 {}\n".format(queue1))
  output.write("queue2 {}\n".format(queue2))
  output.write("queue3 {}\n".format(queue3))
  output.write("ready_queue {} {} {}\n".format(ready_queue[0], ready_queue[1], ready_queue[2]))
  output.write("processing_zakaznici {}\n".format(processing_zakaznici))
  output.write("processing_urednici {}\n".format(processing_urednici))
  output.write("sleeping_urednici {}\n".format(sleeping_urednici))
  output.write("home zakaznici {}\n".format(home_zakaznici))
  output.write("home urednici {}\n".format(home_urednici))
  output.write("all_zakaznici {}\n".format(all_zakaznici))
  output.write("all_urednici {}\n".format(all_urednici))
  # output.write("print_order {}\n".format(print_order)) # sorry tahle funkce je moc dlouhá
  output.write("\n")
  
  if max(wait_zakaznici) == 0:
    output.write("correct wait fronta zákazníků vyprázdněna a přesunuta buď do fronty nebo domů\n")
  else:
    output.write("někteří zákazníci jsou ve fázi čekání a nepřesunuli se do fronty nebo domů v případě zavřené pošty\n")
  
  if max(ready_urednici) == 0:
    output.write("correct všichni úředníci se přesunuli dál (v nejlepším případě domů na konci programu)\n")
  else:
    output.write("někteří úředníci se nedostali domů (nejspíš usnuli v práci)\n")
  
  if max(queue1) == 0:
    output.write("correct všichni zákazníci z queue 1 se přesunuli do spracovávání\n")
  else:
    output.write("někteří zákazníci zůstali v queue 1\n")
  
  if max(queue2) == 0:
    output.write("correct všichni zákazníci z queue 2 se přesunuli do spracovávání\n")
  else:
    output.write("někteří zákazníci zůstali v queue 2\n")
  
  if max(queue3) == 0:
    output.write("correct všichni zákazníci z queue 3 se přesunuli do spracovávání\n")
  else:
    output.write("někteří zákazníci zůstali v queue 3\n")
  
  if max(ready_queue) == 0 and min(ready_queue) == 0:
    output.write("correct počet zákazníku v každé queue má stejný počet spracování od úředníků\n")
  else:
    output.write("počet spracování v nějaké z queue nesedí s počtem zákazníků v dané queue\n")
  
  if max(processing_zakaznici) == 0:
    output.write("correct všichni zákazníci, kteří byli spracováni, šli domů\n")
  else:
    output.write("někteří zákazníci zůstali ve fázi spracovávání\n")
  
  if max(processing_urednici) == 0:
    output.write("correct všichni úředníci dokončili spracovávání a šli zpátky do stavu ready\n")
  else:
    output.write("někteří úredníci zůstali ve fázi spracovávání\n")
  
  if max(sleeping_urednici) == 0:
    output.write("correct všichni úředníci se vyspali a přesunuli se do stavu ready\n")
  else:
    output.write("někteří úředníci se neprobudili ze spánku xd\n")
  
  all_zakaznici = sorted(all_zakaznici)
  home_zakaznici = sorted(home_zakaznici)
  all_urednici = sorted(all_urednici)
  home_urednici = sorted(home_urednici)
  
  if all_zakaznici == home_zakaznici:
    output.write("correct všichni zákazníci se dostali domů\n")
  else:
    output.write("někteří zákazníci se nedostali domů\n")
  
  if all_urednici == home_urednici:
    output.write("correct všichni úředníci se dostali domů\n")
  else:
    output.write("někteří úředníci se nedostali domů\n")
  
  if set(print_order) == set(range(1,(len(print_order) + 1))):
    output.write("correct všechny výpisy jsou očíslovány správně\n")
  else:
    output.write("někde je chyba v číslování výpisů\n")
  
  output.write("error {}\n".format(error))
  output.write("spuštěné parametry použité pro tento výstup: ")
  output.write(str(arg[0]) + " " + str(arg[1]) + " " + str(arg[2]) + " " + str(arg[3]) + " " + str(arg[4]) + "\n")
    
  file.close()
  output.close()

  if(error == 1):
    exit(0)
  """
  (\d*: Z (\d*): started)|(\d*: U (\d*): started)|(\d*: Z (\d*): entering office for a service (\d))|(\d*: U (\d*): serving a service of type \d)|(\d*: Z (\d*): called by office worker)|(\d*: U (\d*): service finished)|(\d*: Z (\d*): going home)|(\d*: U (\d*): taking break)|(\d*: U (\d*): break finished)|(\d*: closing)|(\d*: U (\d*): going home)
  """