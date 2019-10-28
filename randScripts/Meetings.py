"""
--Meeting object--
meeting = {
  "name": "name1",
  "duration": 1 
}
"""

#Maximize number of meetigns

meeting_list = [{
      "name": "meeting1",
      "duration": 2
    },
    {
      "name": "meeting2",
      "duration": 5
    },
    {
      "name": "meeting3",
      "duration": 3
    }]

def optimize(meetings, hours):
    sorted_meetings = sorted(meetings, key=lambda x: x['duration'])
    attended = []
    for m in sorted_meetings:
        if hours - m["duration"] < 0:
            break
        attended.append(m)
        hours -= m["duration"]
    return attended

if __name__ == "__main__":
    m = optimize(meeting_list, 8)
    print(f"Possible Meetings: {m}")
    print(f"Original Meetings: {meeting_list}")