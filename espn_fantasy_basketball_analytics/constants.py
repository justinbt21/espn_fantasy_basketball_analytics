DESC_STATS = ['name'
         , 'position'
         , 'lineupSlot'
         , 'injuryStatus'
]
COUNTING_STATS = [ 'MIN'
         , 'FGM'
         , 'FGA'
         , 'FG%'
         , 'FTM'
         , 'FTA'
         , 'FT%'
         , '3PTM'
         , 'REB'
         , 'AST'
         , 'STL'
         , 'BLK'
         , 'PTS'
         , 'TO'
    ]

ROSTER_COLS = []
FA_COLS = []


def court(shape): 
  court_shapes = []
  if shape == 'half':
    outer_lines_shape = dict(
      type='rect',
      xref='x',
      yref='y',
      x0='-250',
      y0='-47.5',
      x1='250',
      y1='422.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(outer_lines_shape)

    hoop_shape = dict(
      type='circle',
      xref='x',
      yref='y',
      x0='7.5',
      y0='7.5',
      x1='-7.5',
      y1='-7.5',
      line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
      )
    )

    court_shapes.append(hoop_shape)
    backboard_shape = dict(
      type='rect',
      xref='x',
      yref='y',
      x0='-30',
      y0='-7.5',
      x1='30',
      y1='-6.5',
      line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1
      ),
      fillcolor='rgba(10, 10, 10, 1)'
    )

    court_shapes.append(backboard_shape)

    outer_three_sec_shape = dict(
      type='rect',
      xref='x',
      yref='y',
      x0='-80',
      y0='-47.5',
      x1='80',
      y1='143.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(outer_three_sec_shape)

    inner_three_sec_shape = dict(
      type='rect',
      xref='x',
      yref='y',
      x0='-60',
      y0='-47.5',
      x1='60',
      y1='143.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(inner_three_sec_shape)

    left_line_shape = dict(
      type='line',
      xref='x',
      yref='y',
      x0='-220',
      y0='-47.5',
      x1='-220',
      y1='92.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(left_line_shape)

    right_line_shape = dict(
      type='line',
      xref='x',
      yref='y',
      x0='220',
      y0='-47.5',
      x1='220',
      y1='92.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(right_line_shape)

    three_point_arc_shape = dict(
      type='path',
      xref='x',
      yref='y',
      path='M -220 92.5 C -70 300, 70 300, 220 92.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(three_point_arc_shape)

    center_circle_shape = dict(
      type='circle',
      xref='x',
      yref='y',
      x0='60',
      y0='482.5',
      x1='-60',
      y1='362.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(center_circle_shape)

    res_circle_shape = dict(
      type='circle',
      xref='x',
      yref='y',
      x0='20',
      y0='442.5',
      x1='-20',
      y1='402.5',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(res_circle_shape)

    free_throw_circle_shape = dict(
      type='circle',
      xref='x',
      yref='y',
      x0='60',
      y0='200',
      x1='-60',
      y1='80',
      line=dict(
          color='rgba(10, 10, 10, 1)',
          width=1
      )
    )

    court_shapes.append(free_throw_circle_shape)

    res_area_shape = dict(
      type='circle',
      xref='x',
      yref='y',
      x0='40',
      y0='40',
      x1='-40',
      y1='-40',
      line=dict(
        color='rgba(10, 10, 10, 1)',
        width=1,
        dash='dot'
      )
    )
     
    court_shapes.append(res_area_shape)

  elif shape == 'full':
    # point on the center of the court (dummy data)
    midpoint_trace = go.Scatter(
        x = [47],
        y = [25]
    )
     
    # outer boundary
    outer_shape = {
        'type': 'rect',
        'x0': 0,
        'y0': 0,
        'x1': 94,
        'y1': 50,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left backboard
    left_backboard_shape = {
        'type': 'line',
        'x0': 4,
        'y0': 22,
        'x1': 4,
        'y1': 28,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right backboard
    right_backboard_shape = {
        'type': 'line',
        'x0': 90,
        'y0': 22,
        'x1': 90,
        'y1': 28,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left outer box
    left_outerbox_shape = {
        'type': 'rect',
        'x0': 0,
        'y0': 17,
        'x1': 19,
        'y1': 33,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left inner box
    left_innerbox_shape = {
        'type': 'rect',
        'x0': 0,
        'y0': 19,
        'x1': 19,
        'y1': 31,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right outer box
    right_outerbox_shape = {
        'type': 'rect',
        'x0': 75,
        'y0': 17,
        'x1': 94,
        'y1': 33,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right inner box
    right_innerbox_shape = {
        'type': 'rect',
        'x0': 75,
        'y0': 19,
        'x1': 94,
        'y1': 31,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left corner a
    leftcorner_topline_shape = {
        'type': 'rect',
        'x0': 0,
        'y0': 47,
        'x1': 14,
        'y1': 47,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left corner b
    leftcorner_bottomline_shape = {
        'type': 'rect',
        'x0': 0,
        'y0': 3,
        'x1': 14,
        'y1': 3,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right corner a
    rightcorner_topline_shape = {
        'type': 'rect',
        'x0': 80,
        'y0': 47,
        'x1': 94,
        'y1': 47,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right corner b
    rightcorner_bottomline_shape = {
        'type': 'rect',
        'x0': 80,
        'y0': 3,
        'x1': 94,
        'y1': 3,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # half court
    half_court_shape = {
        'type': 'rect',
        'x0': 47,
        'y0': 0,
        'x1': 47,
        'y1': 50,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left hoop
    left_hoop_shape = {
        'type': 'circle',
        'x0': 6.1,
        'y0': 25.75,
        'x1': 4.6,
        'y1': 24.25,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right hoop
    right_hoop_shape = {
        'type': 'circle',
        'x0': 89.4,
        'y0': 25.75,
        'x1': 87.9,
        'y1': 24.25,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left free throw circle
    left_freethrow_shape = {
        'type': 'circle',
        'x0': 25,
        'y0': 31,
        'x1': 13,
        'y1': 19,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right free throw circle
    right_freethrow_shape = {
        'type': 'circle',
        'x0': 81,
        'y0': 31,
        'x1': 69,
        'y1': 19,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # center big circle
    center_big_shape = {
        'type': 'circle',
        'x0': 53,
        'y0': 31,
        'x1': 41,
        'y1': 19,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # center small circle
    center_small_shape = {
        'type': 'circle',
        'x0': 49,
        'y0': 27,
        'x1': 45,
        'y1': 23,
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # left arc shape
    left_arc_shape = {
        'type': 'path',
        'path': 'M 14,47 Q 45,25 14,3',
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # right arc shape
    right_arc_shape = {
        'type': 'path',
        'path': 'M 80,47 Q 49,25 80,3',
        'line': {
            'color': 'rgba(0,0,0,1)',
            'width': 1
        },
    }
     
    # list containing all the shapes
    court_shapes = [
        outer_shape,
        left_backboard_shape,
        right_backboard_shape,
        left_outerbox_shape,
        left_innerbox_shape,
        right_outerbox_shape,
        right_innerbox_shape,
        leftcorner_topline_shape,
        leftcorner_bottomline_shape,
        rightcorner_topline_shape,
        rightcorner_bottomline_shape,
        half_court_shape,
        left_hoop_shape,
        right_hoop_shape,
        left_freethrow_shape,
        right_freethrow_shape,
        center_big_shape,
        center_small_shape,
        left_arc_shape,
        right_arc_shape
    ]

  return court_shapes


  def_distance = ['Overall',
                       '3 Pointers',
                       '2 Pointers',
                       'Less Than 6Ft',
                       'Less Than 10Ft',
                       'Greater Than 15Ft'
                      ]