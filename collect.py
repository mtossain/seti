
if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    
    UpdateRate = 5*60 # In seconds
    DataDir = '/media/michel/SETI'
    # Repeat forever
    while True:

        # start and wait untill next period
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now + ' Started new file')
        tb.start()
        while True:
            NumSeconds = int(time.strftime("%M"))*60+int(time.strftime("%S"))
            if NumSeconds % UpdateRate ==0:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                tb.set_prefix("/media/michel/SETI/" + datetime.now().strftime("%Y/%Y%m%d"))
                time.sleep(1)
                break
            time.sleep(1)
        tb.stop()
        tb.wait()
