dongvat(X):-dongvat_anthit(X);dongvat_anco(X).
dongvat_anco(de).                           % Dê là động vật ăn cỏ.
dongvat_hungdu(soi).                        % Chó sói là động vật hung dữ.
dongvat_anthit(X):-dongvat_hungdu(X).            % Động vật hung dữ là động vật ăn thịt.
an(X,co):-dongvat_anco(X).                  % động vật ăn cỏ thi an co.
an(X,thit):-dongvat_anthit(X).              % động vật ăn thịt thì ăn thịt
an(X,Y):-dongvat_anthit(X),dongvat_anco(Y).      % Động vật ăn thịt ăn các động vật ăn cỏ
uong(X,nuoc):-dongvat_anthit(X);dongvat_anco(X). % Động vật ăn thịt và an co deu uống nước
tieuthu(X,Y):-dongvat(X),(an(X,Y);uong(X,Y)). %Một động vật tiêu thụ cái mà nó uống hoặc cái mà nó ăn.